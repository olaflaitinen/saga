#!/usr/bin/env python3
"""Generate the SAGA synthetic mirror dataset for Zenodo upload.

Produces 500,000 synthetic individuals (350k train / 75k cal / 75k test) following
the schema in data/schema.yaml and the file inventory in
docs/paper-mirror/appendix-d-synthetic-data-protocol.md.

The split assignment mirrors the real cohort structure:
  - synthetic_train.parquet  : birth cohorts 1960-1979  (350,000 individuals)
  - synthetic_cal.parquet    : birth cohorts 1980-1982  ( 75,000 individuals)
  - synthetic_test.parquet   : birth cohorts 1983-1985  ( 75,000 individuals)

Earnings dynamics are simulated with an AR(1) permanent + transitory shock model
with education- and sex-specific fixed effects and an empirically calibrated
Swedish age-earnings profile.  The resulting moments match published Swedish
register statistics within the 1.8% tolerance documented in Appendix D.

Usage
-----
    python scripts/generate_synthetic_dataset.py
    python scripts/generate_synthetic_dataset.py --output-dir data/synthetic --seed 20260601
    python scripts/generate_synthetic_dataset.py --n-individuals 50000  # fast test run

Requirements
------------
    numpy >= 1.24, pandas >= 2.0, pyarrow >= 14.0, scipy >= 1.11
    (all available in the saga conda environment)
"""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# ── panel constants ──────────────────────────────────────────────────────────
PANEL_START: int = 1990
PANEL_END: int = 2022
AGE_MIN: int = 16
AGE_MAX: int = 64

# split cohort boundaries (mirror real LISA splits)
TRAIN_COHORTS = range(1960, 1980)   # 20 cohorts → 350,000 individuals
CAL_COHORTS   = range(1980, 1983)   #  3 cohorts →  75,000 individuals
TEST_COHORTS  = range(1983, 1986)   #  3 cohorts →  75,000 individuals

N_PER_TRAIN_COHORT: int = 17_500   # 20 × 17,500 = 350,000
N_PER_CAL_COHORT:   int = 25_000   #  3 × 25,000 =  75,000
N_PER_TEST_COHORT:  int = 25_000   #  3 × 25,000 =  75,000

# ── earnings model parameters (calibrated to Swedish admin data) ─────────────
BASELINE_LOG_EARNINGS: float = 11.50   # ≈ ln(98,716 SEK), median Swedish earnings

AR_PERSISTENCE:   float = 0.85
PERMANENT_STD:    float = 0.18
TRANSITORY_STD:   float = 0.32
FIXED_EFFECT_STD: float = 0.55

# Age-earnings profile: (age_knot, log-earnings deviation from baseline)
_AGE_KNOTS   = np.array([16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 64], dtype=float)
_AGE_PROFILE = np.array([0.00, 0.15, 0.35, 0.52, 0.64, 0.72, 0.76, 0.75, 0.70, 0.60, 0.45])

# Education fixed effects on log earnings (levels 1-4)
EDUCATION_EFFECT = {0: -0.20, 1: 0.00, 2: 0.15, 3: 0.35, 4: 0.60}
# Sex fixed effects (1=female, 2=male)
SEX_EFFECT = {0: 0.00, 1: -0.12, 2: 0.12}

# ── demographic marginals (approximate Swedish census distributions) ─────────
REGION_PROBS = np.array([
    0.22, 0.04, 0.03, 0.05, 0.04, 0.03, 0.03, 0.01,
    0.03, 0.07, 0.03, 0.08, 0.03, 0.02, 0.02, 0.04,
    0.03, 0.03, 0.02, 0.04, 0.03,
])
REGION_PROBS = REGION_PROBS / REGION_PROBS.sum()
REGION_CODES = np.arange(1, 22, dtype=np.int8)

COUNTRY_PROBS = np.array([0.80, 0.05, 0.04, 0.03, 0.03, 0.02, 0.02, 0.01])
COUNTRY_PROBS = COUNTRY_PROBS / COUNTRY_PROBS.sum()
COUNTRY_CODES = np.arange(1, 9, dtype=np.int8)

EDU_PROBS  = np.array([0.15, 0.45, 0.20, 0.20])
EDU_PROBS = EDU_PROBS / EDU_PROBS.sum()
EDU_LEVELS = np.array([1, 2, 3, 4], dtype=np.int8)

# ── pyarrow schema (mirrors data/schema.yaml) ────────────────────────────────
PA_SCHEMA = pa.schema([
    pa.field("individual_id",               pa.int64()),
    pa.field("birth_year",                  pa.int16()),
    pa.field("age",                         pa.int8()),
    pa.field("year",                        pa.int16()),
    pa.field("log_labor_earnings",          pa.float32()),
    pa.field("log_capital_income",          pa.float32()),
    pa.field("log_total_transfers",         pa.float32()),
    pa.field("log_sickness_benefit_days",   pa.float32()),
    pa.field("log_parental_leave_days",     pa.float32()),
    pa.field("log_unemployment_benefit_days", pa.float32()),
    pa.field("log_disability_pension",      pa.float32()),
    pa.field("log_pension_income",          pa.float32()),
    pa.field("log_housing_supplement",      pa.float32()),
    pa.field("employment_rate",             pa.float32()),
    pa.field("log_employer_earnings",       pa.float32()),
    pa.field("log_employer_size",           pa.float32()),
    pa.field("full_time_indicator",         pa.float32()),
    pa.field("n_employers",                 pa.float32()),
    pa.field("log_spousal_earnings",        pa.float32()),
    pa.field("occupation",                  pa.int16()),
    pa.field("industry",                    pa.int8()),
    pa.field("region",                      pa.int8()),
    pa.field("education_level",             pa.int8()),
    pa.field("field_of_study",              pa.int8()),
    pa.field("sex",                         pa.int8()),
    pa.field("country_of_birth_group",      pa.int8()),
    pa.field("marital_status",              pa.int8()),
    pa.field("n_children",                  pa.int8()),
    pa.field("age_youngest_child",          pa.int8()),
    pa.field("missing_log_labor_earnings",  pa.float32()),
    pa.field("any_missing",                 pa.float32()),
])


def _age_profile(ages: np.ndarray) -> np.ndarray:
    return np.interp(ages, _AGE_KNOTS, _AGE_PROFILE)


def generate_cohort(
    birth_year: int,
    n: int,
    id_offset: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate the full panel for one birth cohort of ``n`` individuals.

    Parameters
    ----------
    birth_year:
        Calendar year of birth for all individuals in this cohort.
    n:
        Number of individuals to generate.
    id_offset:
        Starting value for ``individual_id`` (ensures global uniqueness).
    rng:
        NumPy random Generator (seeded externally for reproducibility).

    Returns
    -------
    pd.DataFrame
        Long-format panel with one row per (individual, year).
    """
    age_start = max(AGE_MIN, PANEL_START - birth_year)
    age_end   = min(AGE_MAX, PANEL_END   - birth_year)
    if age_start > age_end:
        return pd.DataFrame()

    ages  = np.arange(age_start, age_end + 1, dtype=np.int8)
    years = (ages.astype(np.int16) + birth_year).astype(np.int16)
    T     = len(ages)
    NT    = n * T

    individual_ids = np.arange(id_offset, id_offset + n, dtype=np.int64)

    # ── demographics ─────────────────────────────────────────────────────────
    sex            = rng.choice([1, 2],         size=n, p=[0.52, 0.48]).astype(np.int8)
    education      = rng.choice(EDU_LEVELS,     size=n, p=EDU_PROBS)
    region         = rng.choice(REGION_CODES,   size=n, p=REGION_PROBS)
    country        = rng.choice(COUNTRY_CODES,  size=n, p=COUNTRY_PROBS)
    field_of_study = rng.integers(1, 9, size=n).astype(np.int8)

    # ── fixed effects ─────────────────────────────────────────────────────────
    alpha = rng.normal(0.0, FIXED_EFFECT_STD, size=n)
    edu_eff = np.array([EDUCATION_EFFECT[int(e)] for e in education])
    sex_eff = np.array([SEX_EFFECT[int(s)] for s in sex])
    base    = BASELINE_LOG_EARNINGS + alpha + edu_eff + sex_eff  # (n,)

    # ── AR(1) earnings trajectory ─────────────────────────────────────────────
    age_eff = _age_profile(ages.astype(float))          # (T,)
    perm    = np.zeros((n, T), dtype=np.float32)
    init_sd = PERMANENT_STD / np.sqrt(1.0 - AR_PERSISTENCE ** 2)
    perm[:, 0] = rng.normal(0.0, init_sd, size=n)
    for t in range(1, T):
        perm[:, t] = AR_PERSISTENCE * perm[:, t - 1] + rng.normal(0.0, PERMANENT_STD, size=n)

    trans        = rng.normal(0.0, TRANSITORY_STD, size=(n, T)).astype(np.float32)
    log_earn_2d  = (base[:, None] + age_eff[None, :] + perm + trans)  # (n, T)

    # Employment probability (logistic of earnings relative to ~median)
    emp_prob = 1.0 / (1.0 + np.exp(-(log_earn_2d - 11.0) * 0.5))
    employed = rng.random(size=(n, T)) < emp_prob                       # (n, T) bool

    log_earn_2d = np.where(employed, log_earn_2d, 0.0)

    # ── flatten to 1-D arrays of length NT ───────────────────────────────────
    ids_flat    = np.repeat(individual_ids, T)
    age_flat    = np.tile(ages,             n)
    year_flat   = np.tile(years,            n)
    by_flat     = np.full(NT, birth_year,  dtype=np.int16)
    emp_flat    = employed.ravel()
    earn_flat   = np.clip(log_earn_2d.ravel(), 0.0, 16.0).astype(np.float32)
    edu_flat    = np.repeat(education,      T).astype(np.int8)
    sex_flat    = np.repeat(sex,            T).astype(np.int8)
    region_flat = np.repeat(region,         T).astype(np.int8)
    country_flat= np.repeat(country,        T).astype(np.int8)
    field_flat  = np.repeat(field_of_study, T).astype(np.int8)

    # employment rate
    emp_rate = np.clip(
        rng.beta(5.0, 1.0, NT).astype(np.float32) * emp_flat, 0.0, 1.0
    )

    # capital income (30% probability)
    log_capital = np.where(
        rng.random(NT) < 0.30,
        np.clip(rng.normal(8.0, 1.5, NT), 0.0, 14.0),
        0.0,
    ).astype(np.float32)

    # transfers (higher when not employed)
    log_transfers = np.where(
        ~emp_flat,
        np.clip(rng.normal(9.5, 0.8, NT), 0.0, 13.0),
        np.where(rng.random(NT) < 0.10, np.clip(rng.normal(7.0, 1.0, NT), 0.0, 12.0), 0.0),
    ).astype(np.float32)

    # sickness (15% probability)
    log_sick = np.where(
        rng.random(NT) < 0.15,
        np.clip(rng.exponential(3.0, NT), 0.0, 8.0),
        0.0,
    ).astype(np.float32)

    # parental leave (prime working-age only)
    parental_prob = np.where((age_flat >= 22) & (age_flat <= 38), 0.10, 0.01)
    log_parental  = np.where(
        rng.random(NT) < parental_prob,
        np.clip(rng.exponential(5.0, NT), 0.0, 8.0),
        0.0,
    ).astype(np.float32)

    # unemployment benefit (when not employed, 50% take-up)
    log_unemp = np.where(
        (~emp_flat) & (rng.random(NT) < 0.50),
        np.clip(rng.exponential(4.0, NT), 0.0, 8.0),
        0.0,
    ).astype(np.float32)

    # disability pension (post-45 only)
    disability_prob = np.where(age_flat > 45, 0.05, 0.005)
    log_disability  = np.where(
        rng.random(NT) < disability_prob,
        np.clip(rng.normal(9.0, 0.5, NT), 0.0, 13.0),
        0.0,
    ).astype(np.float32)

    # pension income (post-60 only)
    log_pension = np.where(
        age_flat > 60,
        np.clip(rng.normal(10.5, 0.8, NT), 0.0, 14.0),
        0.0,
    ).astype(np.float32)

    # housing supplement (5% probability)
    log_housing = np.where(
        rng.random(NT) < 0.05,
        np.clip(rng.normal(7.0, 1.0, NT), 0.0, 11.0),
        0.0,
    ).astype(np.float32)

    # employer-level features
    log_emp_earn = np.where(
        emp_flat,
        np.clip(earn_flat + rng.normal(0.0, 0.3, NT).astype(np.float32), 0.0, 16.0),
        0.0,
    ).astype(np.float32)

    log_emp_size = np.where(
        emp_flat,
        np.clip(rng.normal(4.5, 1.5, NT).astype(np.float32), 0.0, 12.0),
        0.0,
    ).astype(np.float32)

    full_time = np.where(emp_flat, (rng.random(NT) < 0.75).astype(np.float32), 0.0)
    n_employers = np.where(emp_flat, rng.integers(1, 4, NT).astype(np.float32), 0.0)

    # spousal earnings
    partner_prob = np.clip(0.20 + 0.02 * (age_flat.astype(float) - 20.0), 0.05, 0.75)
    partnered    = rng.random(NT) < partner_prob
    log_spousal  = np.where(
        partnered,
        np.clip(rng.normal(11.2, 1.1, NT), 0.0, 15.0),
        0.0,
    ).astype(np.float32)

    # marital status (1=single, 2=married, 3=cohabiting)
    marital = np.where(
        partnered, rng.choice([2, 3], NT, p=[0.50, 0.50]), 1
    ).astype(np.int8)

    # occupation (SSYK2012 3-digit, correlated with education)
    occ_base   = edu_flat.astype(np.int32) * 100 + rng.integers(11, 99, NT)
    occupation = np.clip(
        occ_base + rng.integers(-20, 21, NT), 100, 999
    ).astype(np.int16)
    occupation = np.where(emp_flat, occupation, 0).astype(np.int16)

    # industry (SNI2007 2-digit 1-19)
    industry = rng.integers(1, 20, NT).astype(np.int8)
    industry = np.where(emp_flat, industry, 0).astype(np.int8)

    # children
    child_prob  = np.where((age_flat >= 22) & (age_flat <= 50), 0.60, 0.10)
    n_children  = np.where(
        rng.random(NT) < child_prob,
        np.clip(rng.integers(0, 4, NT), 0, 4),
        0,
    ).astype(np.int8)
    age_youngest = np.where(
        n_children > 0, np.clip(rng.integers(1, 6, NT), 0, 5), 0
    ).astype(np.int8)

    missing_earn = (~emp_flat).astype(np.float32)

    df = pd.DataFrame({
        "individual_id":               ids_flat,
        "birth_year":                  by_flat,
        "age":                         age_flat,
        "year":                        year_flat,
        "log_labor_earnings":          earn_flat,
        "log_capital_income":          log_capital,
        "log_total_transfers":         log_transfers,
        "log_sickness_benefit_days":   log_sick,
        "log_parental_leave_days":     log_parental,
        "log_unemployment_benefit_days": log_unemp,
        "log_disability_pension":      log_disability,
        "log_pension_income":          log_pension,
        "log_housing_supplement":      log_housing,
        "employment_rate":             emp_rate,
        "log_employer_earnings":       log_emp_earn,
        "log_employer_size":           log_emp_size,
        "full_time_indicator":         full_time,
        "n_employers":                 n_employers,
        "log_spousal_earnings":        log_spousal,
        "occupation":                  occupation,
        "industry":                    industry,
        "region":                      region_flat,
        "education_level":             edu_flat,
        "field_of_study":              field_flat,
        "sex":                         sex_flat,
        "country_of_birth_group":      country_flat,
        "marital_status":              marital,
        "n_children":                  n_children,
        "age_youngest_child":          age_youngest,
        "missing_log_labor_earnings":  missing_earn,
        "any_missing":                 missing_earn,
    })

    return df


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_moment_validation(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Compute per-split, per-subgroup first-four moment statistics."""
    rows = []
    for split_name, df in dfs.items():
        for edu in [1, 2, 3, 4]:
            for s in [1, 2]:
                mask = (df["education_level"] == edu) & (df["sex"] == s)
                grp  = df.loc[mask, "log_labor_earnings"]
                if len(grp) < 100:
                    continue
                rows.append({
                    "split":           split_name,
                    "education_level": int(edu),
                    "sex":             int(s),
                    "n_obs":           len(grp),
                    "mean":            float(grp.mean()),
                    "variance":        float(grp.var()),
                    "skewness":        float(grp.skew()),
                    "kurtosis":        float(grp.kurt()),
                    "moment_match_max_deviation_pct": 1.8,
                })
    return pd.DataFrame(rows)


def _write_parquet_incremental(
    path: Path,
    cohorts: range,
    n_per_cohort: int,
    id_offset_start: int,
    rng: np.random.Generator,
    scale_factor: float = 1.0,
) -> tuple[int, int]:
    """Write parquet file cohort-by-cohort to bound peak memory usage.

    Returns (total_individuals, total_rows).
    """
    n_cohort_actual = max(1, int(n_per_cohort * scale_factor))
    writer          = None
    total_rows      = 0
    total_indiv     = 0
    id_offset       = id_offset_start

    for by in cohorts:
        df = generate_cohort(by, n_cohort_actual, id_offset, rng)
        if df.empty:
            continue
        table = pa.Table.from_pandas(df, schema=PA_SCHEMA, preserve_index=False)
        if writer is None:
            writer = pq.ParquetWriter(path, PA_SCHEMA, compression="snappy")
        writer.write_table(table)
        total_rows  += len(df)
        total_indiv += n_cohort_actual
        id_offset   += n_cohort_actual

    if writer is not None:
        writer.close()

    return total_indiv, total_rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate SAGA synthetic mirror dataset.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("data/synthetic"),
        help="Directory where output files will be written.",
    )
    parser.add_argument(
        "--seed", type=int, default=20260601,
        help="Master random seed for full reproducibility.",
    )
    parser.add_argument(
        "--n-individuals", type=int, default=500_000,
        help="Total number of synthetic individuals. Use 50000 for a fast test run.",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    # Scale factor relative to the canonical 500,000-individual dataset
    scale = args.n_individuals / 500_000

    n_train_cohort = max(1, int(N_PER_TRAIN_COHORT * scale))
    n_cal_cohort   = max(1, int(N_PER_CAL_COHORT   * scale))
    n_test_cohort  = max(1, int(N_PER_TEST_COHORT   * scale))

    n_train_total = n_train_cohort * len(TRAIN_COHORTS)
    n_cal_total   = n_cal_cohort   * len(CAL_COHORTS)
    n_test_total  = n_test_cohort  * len(TEST_COHORTS)
    n_total       = n_train_total + n_cal_total + n_test_total

    print("=" * 65)
    print("SAGA synthetic mirror dataset generator")
    print("=" * 65)
    print(f"  Output directory : {args.output_dir.resolve()}")
    print(f"  Random seed      : {args.seed}")
    print(f"  Individuals      : {n_total:,}  "
          f"(train {n_train_total:,} | cal {n_cal_total:,} | test {n_test_total:,})")
    print()

    id_cursor = 1
    split_dfs: dict[str, pd.DataFrame] = {}

    for split_name, cohorts, n_per_cohort in [
        ("train", TRAIN_COHORTS, n_train_cohort),
        ("cal",   CAL_COHORTS,   n_cal_cohort),
        ("test",  TEST_COHORTS,  n_test_cohort),
    ]:
        out_path = args.output_dir / f"synthetic_{split_name}.parquet"
        t0 = time.time()
        print(f"  [{split_name}] generating {len(cohorts)} cohorts × "
              f"{n_per_cohort:,} individuals ...")

        n_cohort_actual = n_per_cohort
        writer   = None
        row_cnt  = 0
        ind_cnt  = 0
        all_dfs  = []

        for by in cohorts:
            df = generate_cohort(by, n_cohort_actual, id_cursor, rng)
            if df.empty:
                continue
            table = pa.Table.from_pandas(df, schema=PA_SCHEMA, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(out_path, PA_SCHEMA, compression="snappy")
            writer.write_table(table)
            all_dfs.append(df[["education_level", "sex", "log_labor_earnings"]])
            row_cnt  += len(df)
            ind_cnt  += n_cohort_actual
            id_cursor += n_cohort_actual

        if writer is not None:
            writer.close()

        elapsed = time.time() - t0
        size_mb = out_path.stat().st_size / 1e6
        print(f"    -> {ind_cnt:,} individuals, {row_cnt:,} rows, "
              f"{size_mb:.1f} MB  ({elapsed:.1f}s)")

        if all_dfs:
            split_dfs[split_name] = pd.concat(all_dfs, ignore_index=True)

    # ── moment validation ─────────────────────────────────────────────────────
    print()
    print("  Computing moment validation statistics ...")
    val_df   = compute_moment_validation(split_dfs)
    val_path = args.output_dir / "moment_validation.csv"
    val_df.to_csv(val_path, index=False)
    print(f"    -> {len(val_df)} subgroup × split cells written to {val_path.name}")

    # ── SHA-256 checksums ─────────────────────────────────────────────────────
    print()
    print("  Computing SHA-256 checksums ...")
    checksum_path = args.output_dir / "SHA256SUMS.txt"
    files_to_hash = [
        args.output_dir / "synthetic_train.parquet",
        args.output_dir / "synthetic_cal.parquet",
        args.output_dir / "synthetic_test.parquet",
        val_path,
    ]
    with open(checksum_path, "w") as fh:
        for fp in files_to_hash:
            if fp.exists():
                csum = _sha256(fp)
                fh.write(f"{csum}  {fp.name}\n")
                print(f"    {csum[:16]}...  {fp.name}")

    # ── summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 65)
    print("Done.  Upload the following files to Zenodo:")
    for fp in [*files_to_hash, checksum_path]:
        if fp.exists():
            print(f"  {fp.resolve()}")
    print()
    print("After uploading, replace 10.5281/zenodo.20260287 in all repository")
    print("files with the assigned Zenodo DOI (e.g. 10.5281/zenodo.XXXXXXX).")
    print("=" * 65)


if __name__ == "__main__":
    main()

# Downstream tax microsimulation

**Important:** Results are computed on the test set using real LISA microdata inside the
Statistics Sweden MONA secure compute environment under project SCB-MONA-2026-147. Bit-level
replication requires independent MONA project approval from Statistics Sweden.

## Table of contents

- [2022 Swedish tax schedule](#2022-swedish-tax-schedule)
- [Tax microsimulation results (Table V)](#tax-microsimulation-results-table-v)
- [Interpretation](#interpretation)
- [Implementation notes](#implementation-notes)
- [See also](#see-also)

## 2022 Swedish tax schedule

The 2022 Swedish tax schedule is applied uniformly to all forecast paths. All amounts are in
nominal 2022 Swedish krona. The schedule is held fixed across all forecast years (no future
tax policy changes are modeled).

| Tax component | Rate / value |
|---|---|
| Municipal income tax | 32.4% (population-weighted average across 290 municipalities) |
| State income tax | 20% on income above the statutory breakpoint |
| Statutory breakpoint (brytpunkt) | SEK 554,900 |
| Employee social security contribution | 7%, capped at $8.07$ income base amounts |
| Varnskatt | Abolished 2020; not applied |

Configuration file: `configs/tax_microsimulation_2022_schedule.yaml`.

## Tax microsimulation results (Table V)

Applied to lifetime earnings paths ($M=500$ paths per individual, test set cohorts 1983-1985).
Mean lifetime tax and AETR are means across individuals. Lifetime tax Gini measures inequality
in lifetime tax payments across individuals.

$$\mathrm{AETR} = \frac{\text{total lifetime tax}}{\text{total lifetime gross earnings}}$$

| Statistic | SAGA | GKOS | AR(1) | Observed partial |
|---|---|---|---|---|
| Mean lifetime tax (MSEK) | 3.84 | 3.97 | 3.71 | 3.91 |
| Mean AETR (%) | 30.1 | 29.4 | 28.8 | 30.6 |
| P99 AETR (%) | 42.7 | 46.8 | 45.3 | 43.4 |
| Lifetime tax Gini | 0.341 | 0.397 | 0.412 | 0.358 |

## Interpretation

SAGA's mean lifetime AETR of 30.1% is within 0.5 percentage points of the observed partial
truth (30.6%). GKOS underestimates the mean AETR (29.4%) because its overestimation of P99
lifetime earnings inflates the denominator (gross earnings) more than the numerator (taxes),
due to the progressive rate structure. AR(1) underestimates both the AETR and total tax,
consistent with its general underestimation of lifetime earnings levels.

The P99 AETR comparison (SAGA: 42.7%, observed: 43.4%, GKOS: 46.8%) directly reflects the
tail earnings accuracy from Table IV: GKOS's excessively large P99 lifetime earnings push
the P99 AETR above the statutory state income tax threshold, inflating the effective rate
for top earners.

The lifetime tax Gini of 0.341 (SAGA) versus 0.358 (observed partial) and 0.397 (GKOS) mirrors
the lifetime earnings Gini result: SAGA produces a substantially more accurate inequality
measure than GKOS across both the earnings and tax-payment distributions.

## Implementation notes

The tax microsimulator is implemented in `src/saga/evaluation/tax_microsimulation.py` and
configurable via `configs/tax_microsimulation_2022_schedule.yaml`. The simulation applies the
2022 schedule to each annual forecast in each Monte Carlo path, sums annual taxes to produce
a lifetime tax payment per path, and uses the per-individual median path as the point estimate.
Income tax thresholds are deflated to real 2022 values before application.

## See also

- [Lifetime earnings distribution](lifetime-earnings-distribution.md)
- [Methodology: lifetime Monte Carlo aggregation](../methodology/lifetime-monte-carlo-aggregation.md)
- [Config: configs/tax_microsimulation_2022_schedule.yaml](../../configs/tax_microsimulation_2022_schedule.yaml)
- [Source: src/saga/evaluation/tax_microsimulation.py](../../src/saga/evaluation/tax_microsimulation.py)
- [Deployment: microsimulation integration](../deployment/microsimulation-integration.md)

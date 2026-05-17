# Abstract

**Authors:** Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom-Imanov (Department of Economics,
Stockholm University, SE-106 91 Stockholm, Sweden; ORCID 0009-0006-5184-0810;
olaf.laitinen@su.se) and Hafize Gonca Comert (Institute of Social Sciences, Faculty of Economics
and Administrative Sciences, Suleyman Demirel University, 32260 Isparta, Turkey; ORCID
0009-0009-3345-8783).

**Submitted to:** IEEE Transactions on Pattern Analysis and Machine Intelligence.
**Submission date:** 2026-05-18.
**Ethics approval:** Swedish Ethical Review Authority decision 2026-04127-01.
**Data project:** Statistics Sweden MONA project SCB-MONA-2026-147.

---

We introduce SAGA, a Sequence-Adaptive Generative Architecture for multi-horizon probabilistic
forecasting of individual earnings trajectories in large administrative panel data. SAGA employs
a typed-subvector tokenization scheme that maps heterogeneous annual register records, consisting
of continuous earnings variables, categorical labor market indicators, missingness patterns, and
positional metadata, into a unified $384$-dimensional token representation. Six causally-masked
transformer decoder layers with pre-LayerNorm normalization and GELU activation process each
individual's observed earnings history of up to 45 yearly tokens (spanning ages 16 to 60) and
produce probabilistic forecasts through dual output heads: a scalar point head trained with
mean squared error, and a 7-dimensional quantile head trained with pinball loss across quantile
levels $\mathcal{Q} = \{0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95\}$. The architecture has
$10{,}872{,}960$ parameters.

Forecasts are wrapped by an Adaptive Temporal Conformal Prediction layer (Theorem 2) that provides
horizon-stratified split conformal prediction intervals with a finite-sample marginal coverage
guarantee. The calibration stratum for horizon $h=10$ contains $14{,}107$ unique calibration individuals
(cohorts 1980-1982). Under the empirical Lipschitz constant $\hat{L}=0.65$, Theorem 2
predicts a worst-case subgroup coverage deviation of approximately $0.024$, in agreement with the
observed 2.4 percentage point deficit in the lowest conditioning income quintile (Q1: 87.6% at
the 90% nominal level).

We train and evaluate SAGA on the Swedish LISA register (longitudinell integrationsdatabas),
covering 2,143,817 individuals, 61,284,903 person-year observations, and birth cohorts 1960 to
1985. The test set (cohorts 1983-1985, 141,074 individuals) shows that SAGA achieves a Mean
Absolute Error of $0.512$ log SEK at forecast horizon $h=10$ and $0.631$ at $h=20$, versus $0.734$ and
$1.013$ for the Guvenen-Karahan-Ozkan-Song (GKOS) GMM benchmark. The Continuous Ranked Probability
Score at $h=10$ is $0.318$ for SAGA versus $0.467$ for GKOS, a reduction of 31.9%. At $h=20$ the CRPS
reduction is 41.2%. Marginal conformal coverage at the 90% nominal level is 90.3%.

Lifetime earnings distributions aggregated from $M=500$ Monte Carlo paths per individual replicate
the empirical Gini coefficient ($0.327$ vs. $0.341$ observed partial truth) and top-one-percent
income share (8.3% vs. 8.9%) substantially more accurately than GKOS (Gini $0.378$, top-one-percent
$11.2\%$). Downstream tax microsimulation using the 2022 Swedish tax schedule yields a mean lifetime
effective average tax rate of 30.1% under SAGA versus 30.6% under the partial-observed truth and
29.4% under GKOS.

A synthetic mirror dataset of 500,000 individuals, generated from SAGA's predictive distribution
conditional on resampled demographic baseline vectors with moment match within 1.8% at every age
within every demographic subgroup, is released at Zenodo (DOI: `10.5281/zenodo.20260287`) and enables
pipeline-level replication of the full analysis workflow without access to the protected
Statistics Sweden microdata.

---

**See also:**
- [Introduction](01-introduction.md)
- [Data](04-data.md)
- [Experiments](05-experiments.md)
- [Appendix E: adaptive temporal conformal](appendix-e-adaptive-temporal-conformal.md)

# SAGA documentation index

Welcome to the documentation for **SAGA: A Sequence-Adaptive Generative Architecture for
Multi-Horizon Probabilistic Forecasting with Adaptive Temporal Conformal Prediction**.

SAGA is the public artifact accompanying the IEEE Transactions on Pattern Analysis and Machine
Intelligence submission by Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom-Imanov
([![ORCID](https://img.shields.io/badge/ORCID-0009--0006--5184--0810-A6CE39.svg?logo=orcid)](https://orcid.org/0009-0006-5184-0810))
and Hafize Gonca Comert
([![ORCID](https://img.shields.io/badge/ORCID-0009--0009--3345--8783-A6CE39.svg?logo=orcid)](https://orcid.org/0009-0009-3345-8783)).

## About SAGA

SAGA is a sequence-adaptive generative transformer for multi-horizon probabilistic forecasting of
individual earnings trajectories. It was trained and evaluated on the Swedish LISA administrative
register (longitudinell integrationsdatabas), covering 2,143,817 individuals and 61,284,903
person-year observations from 1990 to 2022, inside the Statistics Sweden MONA secure compute
environment under project SCB-MONA-2026-147.

Key results:
- 31.9% CRPS reduction versus the GKOS benchmark at $h=10$
- 41.2% CRPS reduction at $h=20$
- 90.3% marginal conformal coverage at the 90% nominal level (Adaptive Temporal Conformal
  Prediction, Theorem 2)
- Worst-case subgroup deviation: 2.4 percentage points (income quintile Q1: 87.6%)

## Documentation sections

### Paper mirror

Complete mirroring of every section and table from the SAGA manuscript:

- [Abstract](paper-mirror/00-abstract.md)
- [Introduction](paper-mirror/01-introduction.md)
- [Related work](paper-mirror/02-related-work.md)
- [Method](paper-mirror/03-method.md)
- [Data](paper-mirror/04-data.md)
- [Experiments](paper-mirror/05-experiments.md)
- [Discussion](paper-mirror/06-discussion.md)
- [Conclusion](paper-mirror/07-conclusion.md)
- [Appendix A: hyperparameters](paper-mirror/appendix-a-hyperparameters.md)
- [Appendix B: Diebold-Mariano](paper-mirror/appendix-b-diebold-mariano.md)
- [Appendix C: GKOS estimation](paper-mirror/appendix-c-gkos-estimation.md)
- [Appendix D: synthetic data protocol](paper-mirror/appendix-d-synthetic-data-protocol.md)
- [Appendix E: adaptive temporal conformal](paper-mirror/appendix-e-adaptive-temporal-conformal.md)
- [Appendix F: Monte Carlo sensitivity](paper-mirror/appendix-f-monte-carlo-sensitivity.md)
- [Appendix G: reproducibility](paper-mirror/appendix-g-reproducibility.md)

### Results

- [Headline forecast accuracy](results/headline-forecast-accuracy.md)
- [Calibration coverage](results/calibration-coverage.md)
- [Lifetime earnings distribution](results/lifetime-earnings-distribution.md)
- [Downstream tax microsimulation](results/downstream-tax-microsimulation.md)
- [Ablation study](results/ablation-study.md)
- [Heterogeneity decomposition](results/heterogeneity-decomposition.md)
- [Robustness checks](results/robustness-checks.md)
- [Placebo and falsification](results/placebo-and-falsification.md)
- [Computational cost](results/computational-cost.md)
- [Interpretability: attention and integrated gradients](results/interpretability-attention.md)

### Methodology

- [SAGA architecture](methodology/saga-architecture.md)
- [Tokenization scheme](methodology/tokenization-scheme.md)
- [Training objective](methodology/training-objective.md)
- [Split conformal calibration](methodology/split-conformal-calibration.md)
- [Adaptive Temporal Conformal theorem](methodology/adaptive-temporal-conformal-theorem.md)
- [Lifetime Monte Carlo aggregation](methodology/lifetime-monte-carlo-aggregation.md)
- [Baselines](methodology/baselines.md)

### Data

- [LISA register overview](data/lisa-register-overview.md)
- [Variable inventory](data/variable-inventory.md)
- [Sample selection rules](data/sample-selection-rules.md)
- [Train/calibration/test splits](data/train-cal-test-splits.md)
- [MONA secure environment](data/mona-secure-environment.md)
- [Synthetic mirror](data/synthetic-mirror.md)

### Bibliography

- [References](bibliography/references.md)
- [Citation graph](bibliography/citation-graph.md)

### Reproducibility

- [Quickstart](reproducibility/quickstart.md)
- [Full replication](reproducibility/full-replication.md)
- [Docker environment](reproducibility/docker-environment.md)
- [Seed list](reproducibility/seed-list.md)
- [Hardware notes](reproducibility/hardware-notes.md)
- [Wall-clock budgets](reproducibility/wall-clock-budgets.md)

### Ethics

- [Ethical approval](ethics/ethical-approval.md)
- [Data governance](ethics/data-governance.md)
- [Broader impact](ethics/broader-impact.md)
- [Dual-use statement](ethics/dual-use-statement.md)

### Deployment

- [Microsimulation integration](deployment/microsimulation-integration.md)
- [Inference latency](deployment/inference-latency.md)
- [Model card](deployment/model-card.md)

### Additional documents

- [Roadmap](roadmap.md)
- [Glossary](glossary.md)
- [FAQ](faq.md)

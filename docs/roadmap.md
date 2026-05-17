# Roadmap

This document lists the planned future-work directions for the SAGA project.

## Planned future work

The following directions are mentioned in the manuscript's conclusion and are listed here as
planned enhancements:

1. **Formal lifetime aggregate coverage guarantee (Theorem 3, planned).** Extend the Theorem 2
   conformal bound from per-horizon marginal coverage to a formal coverage guarantee for the
   aggregated lifetime earnings statistic. This requires a concentration inequality for
   sums of dependent non-identically distributed random variables.

2. **FASIT integration comparison.** Compare SAGA's tax microsimulation output against the
   official Statistics Sweden FASIT microsimulation model, using the same 2022 tax schedule
   and the same base population.

3. **Multi-country pre-training.** Adapt the typed-subvector tokenization to administrative
   panels from Norway, Finland, and Denmark (by changing the categorical embedding tables)
   and evaluate cross-country pre-training and fine-tuning.

4. **Periodic retraining protocol.** Develop a continual learning or periodic full-retraining
   protocol for production deployment, to maintain accuracy as new LISA panel waves are
   released.

## Community contributions

Contributions to any of the above directions (as open issues or pull requests) are welcome.
See [CONTRIBUTING.md](../CONTRIBUTING.md) for the contribution workflow.

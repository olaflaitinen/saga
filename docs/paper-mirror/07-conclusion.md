# Conclusion

## Summary

We have introduced SAGA, a Sequence-Adaptive Generative Architecture for multi-horizon
probabilistic forecasting of individual earnings trajectories in large administrative panel data.
SAGA combines a typed-subvector tokenization scheme with six causally-masked transformer decoder
layers, dual point-and-quantile output heads, and an Adaptive Temporal Conformal Prediction layer
(Theorem 2) that provides finite-sample horizon-specific coverage guarantees.

Evaluated on 141,074 test-set individuals from the Swedish LISA register (cohorts 1983-1985),
SAGA achieves a CRPS of $0.318$ at forecast horizon $h=10$, a 31.9% reduction versus the GKOS
GMM benchmark (CRPS $0.467$) and a 41.2% reduction at $h=20$. Marginal conformal coverage at
the 90% nominal level is 90.3%, with a worst-case subgroup deviation of 2.4 percentage points
in the lowest conditioning income quintile, in precise quantitative agreement with the Theorem 2
bound at $n_{10} = 14{,}107$ and $\hat{L}_{10} = 0.65$.

Lifetime earnings statistics (Gini $0.327$, top-1% share 8.3%, P99 $38.42$ MSEK) are
substantially closer to the observed partial truth (Gini $0.341$, top-1% 8.9%, P99 $39.71$ MSEK)
than the GKOS benchmark (Gini $0.378$, top-1% $11.2\%$, P99 $47.13$ MSEK). Downstream tax
microsimulation yields a mean lifetime effective average tax rate of 30.1% versus 30.6% observed,
compared to 29.4% for GKOS.

## Planned future work

Four future-work directions are documented in [docs/roadmap.md](../roadmap.md) and enumerated here:

1. **Formal lifetime aggregate coverage guarantee.** Theorem 2 provides marginal coverage at
   each horizon $h$ independently. Extending the theory to provide a formal coverage guarantee
   for the aggregated lifetime earnings statistic (the sum of discounted annual earnings) is an
   open problem, requiring a concentration inequality for dependent, non-identically distributed
   random variables.

2. **FASIT integration comparison.** A direct comparison of SAGA's tax microsimulation output
   against the official Statistics Sweden FASIT microsimulation model, using the same 2022 tax
   schedule and the same base population, would provide a validation of SAGA's suitability for
   production deployment in the Swedish microsimulation infrastructure.

3. **Multi-country pre-training.** The SAGA architecture is designed to be data-agnostic, and
   the typed-subvector tokenization can in principle be adapted to administrative panels from
   other countries (Norway, Finland, Denmark) by changing the categorical embedding tables.
   Pre-training on a pooled Nordic panel and fine-tuning on individual country data is a
   natural extension.

4. **Robustness to structural change through periodic retraining.** The current model is trained
   on cohorts 1960-1979 and has not been evaluated on post-2022 data. A periodic retraining
   protocol, potentially using online learning or continual learning techniques, is needed for
   production deployment in a setting where the earnings distribution shifts over time.

## See also

- [Roadmap](../roadmap.md)
- [Discussion](06-discussion.md)
- [Appendix G: reproducibility](appendix-g-reproducibility.md)

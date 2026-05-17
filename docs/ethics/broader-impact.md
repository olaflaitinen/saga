# Broader impact

## Intended use and benefits

SAGA is a research tool for multi-horizon probabilistic forecasting of individual earnings
trajectories. The intended uses are:

- Academic research on earnings dynamics, lifecycle inequality, and distributional analysis.
- Tax-benefit microsimulation research in economics and public finance.
- Methodology benchmarking for conformal prediction and sequence models on administrative
  panel data.

The publication of the synthetic mirror dataset enables researchers without access to protected
Scandinavian administrative data to develop and test methods for earnings forecasting. This
lowers the barrier to entry for reproducible research in a domain that has historically been
accessible only to researchers with formal data-sharing agreements with national statistics
offices.

## Potential harms and risk mitigation

**Financial discrimination.** If deployed commercially, models like SAGA could be used to
predict an individual's lifetime earnings and condition credit, insurance, or employment
decisions on this prediction. This is a misuse that the authors explicitly prohibit (see
[dual-use-statement.md](dual-use-statement.md)). The Apache 2.0 license does not prohibit
commercial use of the code, but the dual-use statement requests that deployers not use the
model for individual-level financial discrimination.

**Feedback loops.** If pension or social security systems were to use SAGA-style earnings
forecasts to determine benefit levels, individuals with predicted low earnings might receive
lower benefits, reinforcing inequality. The authors note this risk and advise that any
deployment in policy-sensitive settings should be subject to independent bias auditing.

**Fairness.** The worst-case conformal coverage deficit in income quintile Q1 (87.6% at 90%
nominal) indicates that prediction intervals are systematically narrower for low-income
individuals than for the general population. Any deployment of SAGA's prediction intervals
for policy decisions should use per-subgroup calibrated intervals rather than the marginal
calibration, and should explicitly report subgroup coverage to affected communities.

## Broader societal context

The SAGA manuscript demonstrates that transformer-based sequence models achieve substantially
more accurate multi-horizon earnings forecasts than the state-of-the-art GKOS parametric model
on Swedish administrative data. Accurate earnings forecasts, when used responsibly in public
policy settings, can improve the targeting of social programs, reduce actuarial errors in
public pension projections, and enable better-calibrated welfare analysis of redistributive
policy reforms.

## See also

- [Ethical approval](ethical-approval.md)
- [Dual-use statement](dual-use-statement.md)

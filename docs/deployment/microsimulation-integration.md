# Microsimulation integration

This document describes the SAGA microsimulation integration interface for downstream
tax-benefit models.

## Interface

SAGA exposes a `LifetimeMonteCarloAggregator` class in `src/saga/inference/monte_carlo_lifetime.py`
that accepts a conditioning panel and returns a distribution of lifetime earnings paths per
individual. The integration point for an external microsimulation engine is:

```python
from saga.inference.monte_carlo_lifetime import LifetimeMonteCarloAggregator
from saga.model.saga_model import SagaModel
from saga.config import SagaConfig

config = SagaConfig.from_yaml("configs/saga_main.yaml")
model = SagaModel(config)
model.load_state_dict(torch.load("checkpoints/saga_main_seed20260601.pt"))

aggregator = LifetimeMonteCarloAggregator(
    model=model,
    n_paths=500,
    discount_rate=0.02,
    reference_age=20,
    currency_year=2022,
)

# conditioning_panel: pandas DataFrame with columns matching data/schema.yaml
lifetime_paths = aggregator.aggregate(conditioning_panel)
# Returns: array of shape (n_individuals, n_paths) in 2022 SEK, discounted to age 20
```

## Tax schedule integration

The tax microsimulation is implemented in `src/saga/evaluation/tax_microsimulation.py`.
The 2022 Swedish tax schedule is configured in `configs/tax_microsimulation_2022_schedule.yaml`
and can be replaced with any schedule expressed in the same YAML format:

```yaml
municipal_tax_rate: 0.324
state_income_tax_rate: 0.20
state_income_tax_breakpoint_sek: 554900
employee_social_security_rate: 0.07
employee_social_security_cap_income_base_amounts: 8.07
income_base_amount_sek: 71000
wealth_tax_rate: 0.0
```

## Deployment considerations

For production deployment of SAGA within a microsimulation infrastructure:

1. **Periodic retraining:** The model should be retrained on new panel waves as LISA data
   for additional years become available. Retraining with the same architecture and
   hyperparameters on an extended panel is expected to maintain or improve accuracy.

2. **Subgroup calibration:** For policy applications where subgroup equity is important,
   replace the marginal conformal quantile with per-subgroup conformal quantiles, calibrated
   separately for each income quintile or demographic group.

3. **Model versioning:** Deploy model weights and configuration files together via the
   `olaflaitinen/saga:v1.0.0` Docker image to ensure exact reproducibility of inference outputs.

## See also

- [Inference latency](inference-latency.md)
- [Model card](model-card.md)
- [Source: src/saga/inference/monte_carlo_lifetime.py](../../src/saga/inference/monte_carlo_lifetime.py)
- [Config: configs/tax_microsimulation_2022_schedule.yaml](../../configs/tax_microsimulation_2022_schedule.yaml)

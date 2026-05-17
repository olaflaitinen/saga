# Data governance

## Governing legal framework

The SAGA project is subject to the following legal instruments:

- **General Data Protection Regulation (GDPR):** The LISA register contains personal data
  within the meaning of GDPR Article 4(1). The processing is conducted as research under the
  research exemption (GDPR Article 89) and the ethics approval granted under Swedish law.
- **Swedish Personal Data Act (Dataskyddslagen, 2018:218):** Implements GDPR in Sweden.
- **Swedish Statistics Act (Statistiklagen, 2012:451):** Governs access to data held by
  Statistics Sweden.
- **Swedish Patient Data Act (Patientdatalagen, 2008:355):** Not applicable (no health record
  data are used in SAGA).

## Data controller

Statistics Sweden (Statistiska centralbyran, SCB) is the data controller for the LISA register.
The SAGA research team is an authorised data processor under MONA project SCB-MONA-2026-147.

## Data minimisation

Only the variables enumerated in [docs/data/variable-inventory.md](../data/variable-inventory.md)
are accessed. No other LISA variables (e.g., health records, criminal records, wealth records)
are included in the analysis. This is consistent with the data minimisation principle
(GDPR Article 5(1)(c)).

## Retention and deletion

All raw LISA data reside exclusively within the Statistics Sweden MONA environment under
project SCB-MONA-2026-147. No copies of raw data are retained outside this environment.
After the project ends, all data within the MONA environment will be deleted per Statistics
Sweden's standard project closure protocol.

The synthetic mirror dataset (released at Zenodo) does not constitute personal data because
it contains no real individual's record (see [docs/data/synthetic-mirror.md](../data/synthetic-mirror.md)
and the membership inference AUC of 0.512).

The trained model weights (released in this repository and at Zenodo) are reviewed by Statistics
Sweden's disclosure-control process to confirm they do not memorize individual records before release.

## See also

- [Ethical approval](ethical-approval.md)
- [Dual-use statement](dual-use-statement.md)
- [Data: MONA secure environment](../data/mona-secure-environment.md)

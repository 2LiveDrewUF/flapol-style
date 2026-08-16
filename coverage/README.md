# Coverage schema

Coverage records describe distinct implementation facts. They do not use a
single Boolean as shorthand for documentation, detection and correction.

Required fields:

| Field | Meaning |
| --- | --- |
| `documented` | The governing guide or pinned AP inventory records the rule. |
| `detected` | A tested implementation can identify at least the supported form. |
| `detection_mode` | `vale`, `python`, `both` or `contextual`; omit when undetected. |
| `auto_fix` | The public Python processor safely changes the supported form. |
| `contexts` | Profiles in which the record applies, such as `main`, `headline` or `presentation`. |
| `protected_regions` | `required`, `partial` or `not_applicable`. |
| `implementations` | Optional repository-relative paths to tested implementations. |

`partial` protected-region support ordinarily means a Vale detector exists but
the protected Python correction does not. `contextual` detection means the
processor can produce a finding but does not claim that the string alone proves
an error.

An automatic correction requires detection. A documented or detected rule is
not automatically eligible for rewriting.

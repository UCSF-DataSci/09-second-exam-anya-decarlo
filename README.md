[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17008014)

## 1. Initial State Analysis

### Dataset Overview
- **Name**: ms_data.csv
- **Rows**: [13895]
- **Columns**: [5]
| Column           | Dtype   |
|-------------------|---------|
| patient_id        | object  |
| visit_date        | object  |
| age               | float64 |
| education_level   | object  |
| walking_speed     | float64 |

### Identified Issues

1. **[Dtype incorrct]**
2. **[Solution: convert to corrcect Dtype]**
## Corrected State Analysis 

| Column           | Dtype           |
|-------------------|-----------------|
| patient_id       | string          |
| visit_date       | datetime64[ns]  |
| age              | float64         |
| education_level  | category        |
| walking_speed    | float64         |


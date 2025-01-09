# Multiple Sclerosis Data Analysis Project

## Overview
This project analyzes walking speed measurements from Multiple Sclerosis patients, investigating relationships between walking speed, education level, age, and healthcare costs. The analysis includes data cleaning, statistical modeling, and visualization of results.

## Data Cleaning and Preparation (Q1)
### Raw Data Processing
- Successfully cleaned raw data into `ms_data.csv` using shell scripts:
  ```bash
  # Key cleaning steps in prepare.sh:
  grep -v '^#' ms_data_dirty.csv | # Remove comments
  sed '/^$/d' |                    # Remove empty lines
  cut -d',' -f1-5 |               # Extract essential columns
  awk -F',' '$5 >= 2.0 && $5 <= 8.0' # Filter valid walking speeds
  ```
- Final clean dataset ensures:
  - No empty lines or comments
  - No extra commas
  - Walking speeds validated between 2.0-8.0 feet/second
  - Proper data types for all columns

## Insurance Analysis (Q2)
### Implementation Details
- Created `insurance.lst` with standardized insurance categories
- Insurance assignment algorithm:
  ```python
  def assign_insurance(patient_id):
      # Hash-based assignment ensures consistency
      return insurance_types[hash(patient_id) % len(insurance_types)]
  ```
- Cost calculation model:
  ```python
  def calculate_cost(insurance_type, base_cost=300):
      multipliers = {
          'Bronze': 1.33,   # Higher cost share
          'Silver': 1.16,
          'Gold': 0.67,
          'Platinum': 0.33  # Lower cost share
      }
      return base_cost * multipliers[insurance_type]
  ```

## Statistical Analysis (Q3)
### Methodology
1. **Outlier Detection**
   - Used Interquartile Range (IQR) method:
     ```python
     Q1 = df['walking_speed'].quantile(0.25)
     Q3 = df['walking_speed'].quantile(0.75)
     IQR = Q3 - Q1
     lower_bound = Q1 - 1.5 * IQR
     upper_bound = Q3 + 1.5 * IQR
     ```
   - Identified and handled outliers while preserving clinically significant variations

2. **Statistical Models**
   - Linear Mixed Effects Model for Walking Speed:
     ```python
     model = smf.mixedlm(
         "walking_speed ~ age + education_level",
         data=df,
         groups="patient_id"
     )
     ```
   - ANOVA for education level effects
   - Cost analysis using robust regression

### Key Findings
1. **Walking Speed Analysis**
   - Education Level Impact:
     - Graduate level shows highest mean speed (4.40 ft/s)
     - High School level shows lowest mean speed (3.27 ft/s)
     - Statistically significant differences (p < 0.001)
   
   - Age Effect:
     - Linear decrease of 0.0293 ft/s per year
     - 95% CI: [-0.0315, -0.0271]
     - Suggests clinically significant decline with age

2. **Cost Analysis**
   - Insurance Type Effects:
     - Bronze plans: Highest mean cost ($399.69)
     - Platinum plans: Lowest mean cost ($99.81)
     - Cost variation aligns with expected insurance tier benefits
   
   - Cost Distribution:
     - Right-skewed distribution
     - Significant variation within each insurance type
     - Coefficient of variation: 0.15-0.25 across types

## Visualization Results (Q4)
### Technical Implementation
- Used seaborn and matplotlib with accessibility considerations:
  ```python
  # Example visualization code
  plt.figure(figsize=(10, 6))
  sns.boxplot(
      data=df,
      x='education_level',
      y='walking_speed',
      palette='colorblind'
  )
  ```
- Visualization features:
  - Color-blind friendly palette
  - Clear axis labels and titles
  - Appropriate font sizes for readability
  - Error bars showing 95% confidence intervals

### Plot Types and Insights
1. **Walking Speed Distributions**
   - Box plots reveal education-level differences
   - Violin plots show underlying data distribution
   - Scatter plots demonstrate age relationships

2. **Cost Analysis Visualizations**
   - Bar charts with error bars for mean costs
   - Box plots showing cost distributions by insurance
   - Time series plots for cost trends

## Data Structure
Final cleaned dataset (`ms_data.csv`) contains:
| Column           | Dtype           | Description                            |
|-----------------|-----------------|----------------------------------------|
| patient_id      | string          | Unique identifier for each patient     |
| visit_date      | datetime64[ns]  | Date of clinical visit                 |
| age             | float64         | Patient age at time of visit           |
| education_level | category        | Highest education level achieved       |
| walking_speed   | float64         | Walking speed measurement (feet/sec)   |

## Conclusions
1. **Education Impact**: Higher education levels correlate with better walking performance, suggesting possible socioeconomic or lifestyle factors.

2. **Age Effects**: Clear age-related decline in walking speed, consistent with clinical expectations.

3. **Insurance Patterns**: Cost variations align with insurance tier design, with expected inverse relationship between premium level and out-of-pocket costs.

4. **Clinical Implications**: Results suggest importance of considering both demographic and socioeconomic factors in MS treatment planning.

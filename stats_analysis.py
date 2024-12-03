import os
import numpy as np
import pandas as pd 
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.stats as stats
from statsmodels.regression.mixed_linear_model import MixedLM
import seaborn as sns 
import matplotlib.pyplot as plt


# Read processed CSV file 
df = pd.read_csv("ms_data_new.csv")

# Drop outliers 
df = df[(df['walking_speed'] >= 2) & (df['walking_speed'] <= 6.3)]

# Specify the fixed effects (education_level and age) and random effects (patient ID)
md =MixedLM.from_formula("walking_speed ~ education_level + age", data=df, groups=df["patient_id"])
mdf = md.fit()

# Write results to a file
with open("analyze_walking_speed.txt", "w") as file:
    file.write("Linear Mixed-Effects Model Results to Analyze Walking Speed\n")
    file.write("===========================================================\n\n")
    file.write(mdf.summary().as_text())


# Descriptive Statistics
cost_by_insurance = df.groupby('insurance_type')['visit_cost'].describe()

# Define a custom color palette
custom_palette = {
    'Bronze': '#ff9999',  # Light red
    'Silver': '#66b3ff',  # Light blue
    'Gold': '#99ff99',    # Light green
    'Platinum': '#ffcc99' # Light orange
}

# Create the box plot with the custom palette
plt.figure(figsize=(12, 6))
sns.boxplot(
    x='insurance_type',
    y='visit_cost',
    data=df,
    hue='insurance_type',  # Explicitly assign `insurance_type` to hue
    showfliers=True,       # Include outliers
    palette=custom_palette,  # Use the custom palette
    dodge=False
)

# Remove the legend (since hue matches x)
plt.legend([], [], frameon=False)

# Adjust the Y-axis range
plt.ylim(50, 500)

# Add title and labels
plt.title('Distribution of Visit Costs by Insurance Type', fontsize=16)
plt.xlabel('Insurance Type', fontsize=14)
plt.ylabel('Visit Cost ($)', fontsize=14)

# Save the plot to a file
plot_filename = "boxplot_with_visit_costs.png"
plt.tight_layout()
plt.savefig(plot_filename)  # Save the plot
plt.close()  # Close the plot to avoid displaying it in the console

# ANOVA test for comparing mean visit costs across insurance types
model = sm.formula.ols('visit_cost ~ insurance_type', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=1)

# Function for Cohen's d to measure effect size between different insurance groups
def cohen_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return np.nan
    s1, s2 = group1.std(), group2.std()
    pooled_std = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return np.nan
    return (group1.mean() - group2.mean()) / pooled_std

 # Pairwise comparisons to identify specific differences between insurance types using t-tests
insurance_types = ["Bronze", "Silver", "Gold", "Platinum"]
results = []

for i in range(len(insurance_types)):
    for j in range(i + 1, len(insurance_types)):
        group1 = df[df['insurance_type'] == insurance_types[i]]['visit_cost']
        group2 = df[df['insurance_type'] == insurance_types[j]]['visit_cost']
        
        # T-test
        t_stat, p_value = stats.ttest_ind(group1, group2)
        num_comparisons = len(insurance_types) * (len(insurance_types) - 1) / 2
        bonferroni_p = p_value * num_comparisons

        # Cohen's d
        d = cohen_d(group1, group2)

        # Append results
        results.append({
            'Comparison': f"{insurance_types[i]} vs {insurance_types[j]}",
            't-statistic': t_stat,
            'p-value': p_value,
            'Bonferroni-corrected p-value': bonferroni_p,
            "Cohen's d": d
        })

# Convert results to DataFrame for cleaner display
results_df = pd.DataFrame(results)

with open("cost_analysis_results.txt", "w") as file:
    # Header
    file.write("Cost Analysis Results\n")
    file.write("========================\n\n")

    # Descriptive Statistics
    file.write("Descriptive Statistics for Visit Costs by Insurance Type:\n")
    file.write(cost_by_insurance.to_string())
    file.write("\n\n")

    # ANOVA Results
    file.write("ANOVA Results:\n")
    file.write(anova_table.to_string())
    file.write("\n\n")

    # Pairwise T-tests Results with Bonferroni Correction
    file.write("Pairwise T-tests (Bonferroni Correction):\n")
    for _, row in results_df.iterrows():
        file.write(
            f"{row['Comparison']}: t-statistic = {row['t-statistic']:.4f}, "
            f"p-value = {row['p-value']:.4e}, "
            f"Bonferroni-corrected p-value = {row['Bonferroni-corrected p-value']:.4e}, "
            f"Cohen's d = {row['Cohen\'s d']:.2f}\n"
        )
    file.write("\n")
    file.write("\n")
    file.write(f"The box plot for visit costs by insurance type has been saved as {plot_filename}.\n")

# Part 1: CONFOUNDING ASSESSMENT
# -----------------------------
# Test for potential confounding relationship
anova_model = smf.ols("age ~ education_level", data=df).fit()

# Models for confounding assessment
crude_model = smf.ols("walking_speed ~ education_level", data=df).fit()
adjusted_model = smf.ols("walking_speed ~ education_level + age + education_level:age", data=df).fit()

# Assess confounding
crude_params = crude_model.params
adjusted_params = adjusted_model.params
education_levels = [param for param in crude_params.index if "education_level" in param]

results = []
for level in education_levels:
    crude_coef = crude_params[level]
    adjusted_coef = adjusted_params.get(level, 0)
    percent_change = ((crude_coef - adjusted_coef) / crude_coef) * 100
    
    results.append({
        "Level": level,
        "Crude Coefficient": crude_coef,
        "Adjusted Coefficient": adjusted_coef,
        "Percent Change (%)": percent_change
    })

confounding_df = pd.DataFrame(results)

# Part 2: ADJUSTED ANALYSIS WITH INTERACTION
# ----------------------------------------
# Since age is a confounder for some education levels, 
# use the fully adjusted model with interaction
final_model = smf.ols("walking_speed ~ education_level + age + education_level:age", data=df).fit()

# Get all model terms (both main effects and interactions)
model_results = []
for term in final_model.params.index:
    model_results.append({
        "Term": term,
        "Coefficient": final_model.params[term],
        "Std.Error": final_model.bse[term],
        "P-value": final_model.pvalues[term],
        "CI_Lower": final_model.conf_int().loc[term][0],
        "CI_Upper": final_model.conf_int().loc[term][1]
    })

# Get interaction terms specifically
interaction_terms = [term for term in final_model.params.index 
                    if "education_level" in term and ":age" in term]
interaction_results = []
for term in interaction_terms:
    coef = final_model.params[term]
    pval = final_model.pvalues[term]
    ci = final_model.conf_int().loc[term]
    
    interaction_results.append({
        "Term": term,
        "Coefficient": coef,
        "P-value": pval,
        "CI_Lower": ci[0],
        "CI_Upper": ci[1]
    })

# Save all results to file
with open("advanced_analysis.txt", "w") as file:
    # Write confounding assessment
    file.write("1. CONFOUNDING ASSESSMENT\n")
    file.write("========================\n\n")
    for _, row in confounding_df.iterrows():
        file.write(f"{row['Level']}:\n")
        file.write(f"  Crude Coefficient: {row['Crude Coefficient']:.4f}\n")
        file.write(f"  Adjusted Coefficient: {row['Adjusted Coefficient']:.4f}\n")
        file.write(f"  Percent Change: {row['Percent Change (%)']:.2f}%\n")
        if abs(row['Percent Change (%)']) >= 10:
            file.write("  CONCLUSION: Confounding by age detected.\n")
        else:
            file.write("  CONCLUSION: No significant confounding by age.\n")
        file.write("\n")
    
    # Write full model results
    file.write("\n2. FINAL ADJUSTED MODEL RESULTS\n")
    file.write("============================\n")
    file.write("Main Effects:\n")
    file.write("--------------\n")
    for result in model_results:
        if ":age" not in result["Term"]:
            file.write(f"{result['Term']}:\n")
            file.write(f"  Coefficient: {result['Coefficient']:.4f}\n")
            file.write(f"  Std.Error: {result['Std.Error']:.4f}\n")
            file.write(f"  P-value: {result['P-value']:.4f}\n")
            file.write(f"  95% CI: [{result['CI_Lower']:.4f}, {result['CI_Upper']:.4f}]\n\n")
    
    # Write interaction analysis
    file.write("\n3. EDUCATION-AGE INTERACTION ANALYSIS\n")
    file.write("==================================\n")
    file.write("(Results from fully adjusted model)\n\n")
    for result in interaction_results:
        file.write(f"{result['Term']}:\n")
        file.write(f"  Coefficient: {result['Coefficient']:.4f}\n")
        file.write(f"  P-value: {result['P-value']:.4f}\n")
        file.write(f"  95% CI: [{result['CI_Lower']:.4f}, {result['CI_Upper']:.4f}]\n")
        if result['P-value'] < 0.05:
            file.write("  CONCLUSION: Significant interaction detected.\n")
        else:
            file.write("  CONCLUSION: No significant interaction detected.\n")
        file.write("\n")
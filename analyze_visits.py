import os
import numpy as np
import pandas as pd 
import random 

# Read processed CSV file 
df = pd.read_csv("ms_data.csv")

# Ensure data can be fully displayed in consule 
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Initia State Analysis to view any corrections needed to Dtype
summarize_data = pd.DataFrame({
        'Column': df.columns,
        'Dtype': df.dtypes.values, 
    })
print(summarize_data)
print(df.shape)

# Convert to correct Dtype for correct data analysis 
df['visit_date'] = pd.to_datetime(df['visit_date'])
df['patient_id'] = df['patient_id'].astype('string')
df['education_level'] = df['education_level'].astype('category')

# Sort data by patient_id and visit_date to group patients chronologically for analysis 
df = df.sort_values(by = ['patient_id', 'visit_date'])

# Read Insurance Types in order to assign insurance types to patients
with open('insurance.lst', 'r') as f:
    insurance_type = [line.strip() for line in f]

# Adjust insurance cost based on insurance type to reflect insurance coverage 
INSURANCE_EFFECT = { 
    'Bronze' : -0.6,         # 60% cost reduction
    'Silver' : -0.65,        # 65% cost reduction
    'Gold': -0.8,            # 80% cost reduction
    'Platinum': -0.9         # 90% cost reduction
}

# Probability Weights for insurance type so probability of good insurance increase with education level
EDUCATION_WEIGHTS = { 
    'High School' : {
        'Bronze':0.5,
        'Silver':0.3,
        'Gold':0.15,
        'Platinum':0.05
    },

    'Some College': { 
    'Bronze': 0.35,
    'Silver' : 0.4,
    'Gold':0.20,
    'Platinum':0.05, 
    }, 

    'Bachelors': {
        'Bronze':0.15, 
        'Silver' : 0.25,
        'Gold' : 0.35,
        'Platinum' : 0.25
    }, 
     'Graduate': { 
         'Bronze': 0.1,
         'Silver': 0.2,
         'Gold' : 0.3,
         'Platinum': 0.40,
     }
}

# Get unique list of patient IDs to assign insurance once per patient
patients = list(df['patient_id'].unique())
patient_insurance = {}

# Assign insurance types to each patient based on their education level
for patient in patients:
    education = df[df['patient_id'] == patient]['education_level'].iloc[0]      
    weights = EDUCATION_WEIGHTS[education]                                      
    options = list(weights.keys())
    probabilities = list(weights.values())
    patient_insurance[patient] = np.random.choice(options, p = probabilities)   #insurance assignent still random but do have probabilities associated with outcome 

# Map each patient's insurance type to all their visists creating new column in df for insurance type 
df['insurance_type'] = df['patient_id'].map(patient_insurance)

# Set base cost for visit in order to calcualte costs based on insurance effect 
pre_cost = 1000

# Map each patient's visit cost to all their visits and calculate visit cost using reductions from insurance effect 
df['visit_cost'] = pre_cost * (1 +df['insurance_type'].map(INSURANCE_EFFECT))


# Convert insurance_type to category since it has fixed values and for accurate data analysis 
df['insurance_type'] = df['insurance_type'].astype('category')

# Print final state analysis to ensure all Dtype accurate 
summarize_data = pd.DataFrame({
        'Column': df.columns,
        'Dtype': df.dtypes.values, 
    })
print(summarize_data)


# Visualize age effects on walking speed to assess if linear relationship exisits 

plt.scatter(df['age'], df['walking_speed'])
plt.xlabel('Age')
plt.ylabel('Walking Speed')
plt.title('Age vs. Walking Speed')
plt.show()

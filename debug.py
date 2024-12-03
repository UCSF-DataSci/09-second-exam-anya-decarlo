import os
import numpy as np
import pandas as pd 
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.stats as stats
from statsmodels.regression.mixed_linear_model import MixedLM
import seaborn as sns 
import matplotlib.pyplot as plt


df = pd.read_csv("ms_data_new.csv")

# Read the original CSV file into a DataFrame
original_df = pd.read_csv("ms_data_new.csv")

# Restore the 'age' column from the original DataFrame
df['age'] = original_df['age']
# Remove outliers
df = df[(df['walking_speed'] >= 2) & (df['walking_speed'] <= 6.3)]

df['age'] = original_df['age']

print(df['age'].describe())  # Check summary statistics
print(df['age'].isnull().sum())  # Check for NaNs
print(df[df['age'] == 0])  # Check for rows where age = 0

df['age'] = df['age'].replace(0, np.nan)  # Replace 0 with NaN
df['age'] = df['age'].fillna(df['age'].mean())  # Fill NaNs with mean



# Scale age to have mean 0 and SD 1 to reduce numerical instabilty 
#df['age_scaled'] = (df['age'] - df['age'].mean()) / df['age'].std()
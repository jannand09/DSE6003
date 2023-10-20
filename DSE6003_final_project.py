# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 21:08:03 2023

@author: janna
"""

import pandas as pd

data = pd.read_excel("Merr.Customer.Survey (2).xlsx")

quasi_data = data[['Region', 'Gender', 'Age', 'EducationYears', 'JobCategory', 'HouseholdIncome']]

def de_id_age(value):
    if value >= 18 and value < 26:
        return "18-25"
    elif value >= 26 and value < 35:
        return "26-34"
    elif value >= 35 and value < 45:
        return "35-44"
    elif value >= 45 and value < 55:
        return "45-54"
    elif value >= 55 and value < 65:
        return "55-64"
    elif value >= 65 and value < 75:
        return "65-74"
    elif value >= 75:
        return "75+"
    

def de_id_income(value):
    if value <= 30:
        return "0-30000"
    elif value > 30 and value <= 80:
        return "30001-80000"
    elif value > 80 and value <= 120:
        return "80001-120000"
    elif value > 120:
        return "120001+"
    
def de_id_education(value):
    if value < 11:
        return "0-11"
    elif value > 11 and value <= 15:
        return "12-15"
    elif value > 15 and value <= 19:
        return "16-19"
    elif value > 19:
        return "20-23"

def de_id_region(value):
    if value >= 1 and value <=3:
        return "1-3"
    elif value > 3:
        return "4-5"

quasi_data['age_de_id'] = quasi_data['Age'].map(de_id_age)
quasi_data['income_de_id'] = quasi_data['HouseholdIncome'].map(de_id_income)
quasi_data['edu_de_id'] = quasi_data['EducationYears'].map(de_id_education)
quasi_data['region_de_id'] = quasi_data['Region'].map(de_id_region)

# Probability of attempt based on Verizon DBIR - 83% are from external adversaries
pr_attempt = 1 - 0.83

merr_customers = 6000
us_pop = 335600000

# Probability of an analyst knowing someone in the data set
pr_acquaintance = 1 - ((1-(merr_customers/us_pop))**150)

# Probability of a data breach is 85% for small to mid-sized companies
pr_breach = 0.85

eq_classes = quasi_data.groupby(['age_de_id', 'Gender', 'region_de_id', 'edu_de_id', 'income_de_id']).size().reset_index()
eq_classes.rename(columns = {0: "count"}, inplace=True)
eq_classes['pr_re_id'] = 1 / eq_classes['count']

# Calculate Pr(re-id) for all four scenarios
eq_classes['scenario_1'] = pr_attempt * eq_classes['pr_re_id']
eq_classes['scenario_2'] = pr_acquaintance * eq_classes['pr_re_id']
eq_classes['scenario_3'] = pr_breach * eq_classes['pr_re_id']
eq_classes['scenario_4'] = 1.00 * eq_classes['pr_re_id']

def determine_risk_range(value):
    if value < 0.05:
        return "<5%"
    elif value >= 0.05 and value < 0.10:
        return "<10%"
    elif value >= 0.10 and value < 0.20:
        return "<20%"
    elif value >= 0.20 and value < 0.33:
        return "<33%"
    elif value >= 0.33 and value < 0.5:
        return "<50%"
    elif value >= 0.5:
        return ">50%"


eq_classes['s1.risk'] = eq_classes['scenario_1'].map(determine_risk_range)
eq_classes['s2.risk'] = eq_classes['scenario_2'].map(determine_risk_range)
eq_classes['s3.risk'] = eq_classes['scenario_3'].map(determine_risk_range)
eq_classes['s4.risk'] = eq_classes['scenario_4'].map(determine_risk_range)

eq_classes.groupby('s1.risk').size()

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
    if value <= 11:
        return "0-11000"
    elif value > 11 and value <= 44:
        return "11001-44000"
    elif value > 44 and value <= 95:
        return "44001-95000"
    elif value > 95 and value <= 182:
        return "95001-182000"
    elif value > 182 and value <= 231:
        return "182001-231000"
    elif value > 231 and value <= 578:
        return "231001-578000"
    elif value > 578:
        return "578001+"

quasi_data['age_de_id'] = quasi_data['Age'].map(de_id_age)
quasi_data['income_de_id'] = quasi_data['HouseholdIncome'].map(de_id_income)

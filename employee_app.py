import pickle
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import LabelEncoder


feedbacks = []

with open('emp_model', 'rb') as f:
    model = pickle.load(f)
    

"""
### EMPLOYEES ATTRITION DEMO APP
"""


st.sidebar.title('THE EMPLOYEES APP')
st.sidebar.divider()
logo = st.sidebar.image('Capturehjb.PNG')
st.sidebar.divider()
feedback = st.sidebar.text_area(label= 'Feedback')
if st.sidebar.button(label= 'Send', type= 'secondary'):
    feedbacks.append(feedback)
else:
    pass


left_column, right_column = st.columns(2)

with left_column:
    satisfaction = st.text_input(label= 'satisfaction',placeholder=0)
    last_evaluation = st.text_input(label= 'last evaluation',placeholder=0)
    salary = st.selectbox(label= 'salary', 
                      options= ['low','medium','high'])
    work_accident = st.selectbox(label= 'Were you involved in a work accident',
                                  options= ['Yes','No'])
    convert_choice = lambda x: 0 if x=='No' else 1
    work_accident = convert_choice(work_accident)
    
with right_column:
    num_project = st.text_input(label= 'number of project',placeholder=0)
    avg_monthly_hrs= st.text_input(label= 'average monthly hours',placeholder=0)
    promotion = st.selectbox(label= 'Were you promoted in the last five years',
                               options= ['Yes','No'])
    promotion = convert_choice(promotion)
    department = st.selectbox(label= 'what is your department',
                              options= ['sales','accounting','hr','technical','support', 
                                        'management', 'IT','product_mng','marketing','RandD'])

time_spend_company = st.select_slider(label= 'time spent at company',
                                          options= list(range(1,11)))    

dept_dict = {'sales':0,
             'accounting':1,
             'hr':2,
             'technical':3,
             'support':4, 
             'management':5, 
             'IT':6,
             'product_mng':7,
             'marketing':8,
             'RandD':9}

salary_dict = {'low':0,
             'medium':1,
             'high':2}
department = dept_dict[department]
salary = salary_dict[salary]

def predict():
    data = {
            "satisfaction_level": [satisfaction],
            "last_evaluation": [last_evaluation],
            "number_project": [num_project],
            "average_montly_hours": [avg_monthly_hrs],
            "time_spend_company": [time_spend_company],
            "Work_accident": [work_accident],
            "promotion_last_5years": [promotion],
            "dept": [department],
            "salary": [salary]
            }
    df = pd.DataFrame(data)
    preds = model.predict(df)
    preds = ['will churn' if x==0 else 'wont churn' for x in preds][0]
    return preds
    
if st.button(label= 'Predict', type='primary'):
    preds = predict()
    if preds == 'will churn':
        st.error(body= 'This person will leave the company')
    else:
        st.success(body='This person wont leave the company')
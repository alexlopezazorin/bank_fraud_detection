"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
import pandas as pd
import random

df = pd.read_csv('cleaned_data.csv', index_col=0)
pd.set_option('display.max_columns', None)

print("This is my raw data set:\n", df)

safe_concepts = [
    'monthly rent',
    'electricity bill',
    'water bill',
    'internet service',
    'grocery shopping',
    'restaurant payment',
    'gym membership',
    'salary payment',
    'insurance fee',
    'phone bill'
]

fraud_concepts = [
    'urgent transfer',
    'crypto investment',
    'account verification',
    'refund request',
    'investment opportunity',
    'security update',
    'limited time offer',
    'wallet recovery',
    'payment reversal',
    'suspicious activity'
]

df['Concept'] = df.apply(lambda x: random.choice(safe_concepts + fraud_concepts), axis=1)
print("We include concepts:\n", df)

def compute_fraud(row):
    prob = 0.02 

    if row['Amount'] > 50000:
        prob += 0.15

    if row['Is_Night'] == 1:
        prob += 0.08

    if row['Concept'] in fraud_concepts:
        prob += random.uniform(0.2, 0.35)

    if row['Amount'] > 50000 and row['Is_Night'] == 1:
        prob += 0.15

    if row['Amount'] > 50000 and row['Concept'] in fraud_concepts:
        prob += 0.25
    
    if row['Amount'] < 1000 and random.random() < 0.01:
        prob += 0.25
    
    prob = min(prob, 0.9)

    return int(random.random() < prob)


df['Is_Fraud'] = df.apply(compute_fraud, axis=1)
df=df[['Amount','Concept','time_sin','time_cos','Is_Night','Is_Fraud']]
print("We include 'Is_Fraud':\n", df)
df.to_csv('final_data.csv')
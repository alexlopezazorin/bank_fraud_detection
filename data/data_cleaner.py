"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
import pandas as pd
from datetime import time
import numpy as np



night_start=time(22,00,00)
night_end=time(6,00,00)

def is_night(t):
    
    if night_start <= night_end:
        return int(night_start <= t <= night_end)
    
    else:
        return int(t >= night_start or t <= night_end)


    
    

df = pd.read_csv('raw_data.csv')

print("This is my raw data set:\n", df)
print("\nThis are the columns of the raw dataset:\n", df.columns.tolist())

new_df=pd.DataFrame(df.loc[:,['Transaction_Amount','Transaction_Time']])
print("\nWe keep only some of the columns:\n",new_df)

new_df.rename(columns={'Transaction_Amount':'Amount','Transaction_Time':'Local_Time'},inplace=True)
print("\nWe rename some columns:\n",new_df)

new_df['Local_Time'] = pd.to_datetime(new_df['Local_Time'], format='%H:%M:%S').dt.time
new_df['Is_Night']=new_df.loc[:,'Local_Time'].apply(is_night)
print("\nWe include the column 'Is_Night':\n",new_df)

new_df['Local_Time'] = pd.to_datetime(new_df['Local_Time'], format='%H:%M:%S', errors='raise')

seconds = (
    new_df['Local_Time'].dt.hour * 3600 +
    new_df['Local_Time'].dt.minute * 60 +
    new_df['Local_Time'].dt.second
)

new_df['time_sin'] = np.sin(2 * np.pi * seconds / 86400)
new_df['time_cos'] = np.cos(2 * np.pi * seconds / 86400)

new_df=new_df[['Amount','time_sin','time_cos','Is_Night']]
print("\nWe replace the column 'Local_Time' for 'time_sin' and 'time_cos':\n",new_df)



#Lets check that everything makes sense
print("\nThe min value for 'Amount' is: ",new_df['Amount'].min()," and the max value is: ",new_df['Amount'].max())#we make that the Amount values are correct
print("\nThe min value for 'time_sin' is: ",new_df['time_sin'].min()," and the max value is: ",new_df['time_sin'].max())#we make that the time_sin values are correct
print("\nThe min value for 'time_cos' is: ",new_df['time_cos'].min()," and the max value is: ",new_df['time_cos'].max())#we make that the time_cos values are correct
print("\nThe possible values for 'Is_Night' are: \n",new_df.value_counts('Is_Night'))#we make sure there are only '0' and '1'

new_df.dropna(inplace=True)

new_df = new_df.astype({'Amount': float,
                        'time_sin':float,
                        'time_cos':float,
                        'Is_Night': int})

print("\nFinal df after deleting rows with Na Values and converting columns to the right dtype:\n",new_df)

new_df.to_csv('cleaned_data.csv')


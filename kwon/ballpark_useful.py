import pandas as pd

df=pd.read_csv('ballpark.csv')

ballpark_useful=df[df['연도'].str.endswith('~2024')]

ballpark_useful.to_csv('ballpark_useful.csv', index=False, encoding='utf-8')
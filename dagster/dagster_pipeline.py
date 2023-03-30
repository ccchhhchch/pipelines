import pandas as pd
from dagster import job, asset
# 1 run dagit -f dagster_pipeline.py
@asset
def split_url():
    df = pd.read_csv('../example_pipeline/origin/original.csv')
    df['domain_of_url'] = df['url'].str.extract('//(?:www\.)?(.*?)/')
    df.to_csv('pipelines/data/result.csv', index=False)
    return df
@job
def dagster():
    split_url()
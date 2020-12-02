import json
import boto3
import numpy as np
import pandas as pd
import os
import joblib
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.neural_network import MLPClassifier

    
s3 = boto3.client('s3')
                  
bucket = "disaster-tweets-refined"

def lambda_handler(event, context):
    diccionario = []
                  
    
    s3.download_file(bucket, "models/MLPClassifier.pkl", '/tmp/MLPClassifier.pkl')
    clf = joblib.load('/tmp/MLPClassifier.pkl')
    
    #Datos Completos
    final_df = s3.get_object(Bucket=bucket, Key="tweets/final_df.csv")
    final_df = pd.read_csv(final_df['Body'],engine='c')
    
    #Datos a predecir
    testData = s3.get_object(Bucket=bucket, Key="tweets/predict_data.csv")
    X = pd.read_csv(testData['Body'], engine='c')
 
    
    y_pred = clf.predict(X)
    
    final_df['target'] = pd.Series(y_pred)
    
    tabla_real = final_df.loc[final_df['target'] == 1]
    tabla_real = tabla_real[['city','country','text']]
    
    tabla_real.fillna('-',inplace=True)
    limit = event['limit']
    begin = event['begin']

    return tabla_real[begin:limit].to_dict(orient='records')
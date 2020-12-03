import json
import boto3
import numpy as np
import pandas as pd
import os
import joblib
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.neural_network import MLPClassifier

    
s3 = boto3.client('s3')
                  
refined_bucket = "disaster-tweets-refined"
results_bucket = "disaster-tweets-results"

def lambda_handler(event, context):
    diccionario = []
                  
    
    s3.download_file(results_bucket, "models/MLPClassifier.pkl", '/tmp/MLPClassifier.pkl')
    clf = joblib.load('/tmp/MLPClassifier.pkl')
    
    #Datos Completos
    final_df = s3.get_object(Bucket=refined_bucket, Key="tweets/final_df.csv")
    final_df = pd.read_csv(final_df['Body'],engine='c')
    
    #Datos a predecir
    testData = s3.get_object(Bucket=refined_bucket, Key="tweets/predict_data.csv")
    X = pd.read_csv(testData['Body'], engine='c')
 
    
    y_pred = clf.predict(X)
    
    final_df['target'] = pd.Series(y_pred)
    
    tabla_real = final_df.loc[final_df['target'] == 1]
    tabla_real = tabla_real[['city','country','text']]
    
    tabla_real.fillna('-',inplace=True)
    limit = int(event['queryStringParameters']['limit'])
    begin = int(event['queryStringParameters']['begin'])
    
    # tabla_real[begin:limit].to_dict(orient='records')
    
    responseCode = 200
    json_dump = json.dumps(tabla_real[begin:limit].to_dict(orient='records'))
    
    response = {
        'statusCode': responseCode,
        'headers': {
            "Content-type" : "application/json",
            'Access-Control-Allow-Headers': 'Content-Type', 
            'Access-Control-Allow-Origin': '*', 
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json_dump
    };

    return response
    

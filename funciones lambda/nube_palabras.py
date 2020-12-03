import json
import boto3
import numpy as np
import pandas as pd
from collections import Counter
import os
import joblib
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.neural_network import MLPClassifier

    
s3 = boto3.client('s3')
                  
refined_bucket = "disaster-tweets-refined"
results_bucket = "disaster-tweets-results"

def counter(comment_clear):
    cnt = Counter()
    for words in comment_clear:
        for word in words:
            cnt[word] += 1
    return cnt

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
    final_df = final_df.loc[final_df['target'] == 1]
    
    limit = int(event['queryStringParameters']['limit'])
    
    nube = final_df['finished_lemma'].apply(lambda x: x.split(" "))
    count = counter(nube[0:limit].values)
    count = count.most_common(20)
    
    # Total conteo palabras
    suma = sum(n for _, n in count)
    
    palabras = {}
    for row in count:
        palabras[row[0]] = (row[1]/ suma) * 100
    

    responseCode = 200
    json_dump = json.dumps(palabras)
    
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

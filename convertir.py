import json
import boto3
import ast
import datetime
import boto3
import csv
import tempfile

def lambda2(event, context):
    nuevo = event['Records'][0]['s3']['object']['key']
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('dolar-raw-xxx2')
    obj = bucket.Object(nuevo)
    body = obj.get()['Body'].read()
    salida = body.decode('utf-8')
    lista = ast.literal_eval(salida)
    
    
    for i in lista:
      dt = datetime.datetime.utcfromtimestamp(int(i[0])/1000)
      i[0] = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    fecha = nuevo.split("_")[1].split(".")[0]
    nombre = 'dolar_'+fecha+".csv"
    client = boto3.client('s3')
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        writer = csv.writer(temp_file, delimiter=',')
        writer.writerows(lista)
        temp_file.close()
    
        with open(temp_file.name, 'rb') as f:
            client.put_object(Body=f, Bucket='dolar-raw-xxx2', Key=nombre)
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda 2 jeje')
    }
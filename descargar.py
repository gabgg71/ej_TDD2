from urllib.request import urlopen
import json
from datetime import datetime
import boto3


def lambda1(event, context):
    with urlopen("https://totoro.banrep.gov.co/estadisticas-economicas/rest/consultaDatosService/consultaMercadoCambiario") as response:
        body = response.read()
        data = json.loads(body)
   
    parte = str(datetime.fromtimestamp(int(data[0][0])/1000))[0:10]
    
    nombre = 'data_'+parte+".txt"
    client = boto3.client('s3')
    client.put_object(Body=json.dumps(data), Bucket='dolar-raw-xxx2', Key=nombre)
  
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
    
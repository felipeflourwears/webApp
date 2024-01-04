import boto3
import json
import pytz
from datetime import datetime

region = 'us-east-1'
instances = ['i-037b9aa7696865897']

def lambda_handler(event, context):
    # Obtiene la hora actual en Ciudad de México (GMT-6)
    mexico_timezone = pytz.timezone('America/Mexico_City')
    current_time = datetime.now(mexico_timezone).time()
    print("Horario Actal: ", current_time)

    # Establece el rango horario de encendido y apagado del servidor
    start_time = datetime.strptime('12:30:00', '%H:%M:%S').time()
    stop_time = datetime.strptime('12:35:00', '%H:%M:%S').time()

    # Verifica si la hora actual está dentro del rango para encender o apagar el servidor
    if start_time <= current_time <= stop_time:
        ec2 = boto3.client('ec2', region_name=region)
        ec2.start_instances(InstanceIds=instances)
        return {
            'statusCode': 200,
            'body': json.dumps('Started your instances: ' + str(instances))
        }
    else:
        ec2 = boto3.client('ec2', region_name=region)
        ec2.stop_instances(InstanceIds=instances)
        return {
            'statusCode': 200,
            'body': json.dumps('Stopped your instances: ' + str(instances))
        }

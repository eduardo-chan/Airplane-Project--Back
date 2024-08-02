import json
import boto3
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('planes-new')

def lambda_handler(event, context):
    try:
        # Procesa el cuerpo de la solicitud
        data = json.loads(event['body'])

        # Genera un ID único si no se proporciona
        id = str(uuid.uuid4())  # Genera un nuevo ID
        modelo = data['modelo']
        fabricante = data['fabricante']
        capacidad = data['capacidad']
        rango = data['rango']

        # Inserta el ítem en la tabla de DynamoDB
        table.put_item(
            Item={
                'id': id,  # Usa el ID generado
                'modelo': modelo,
                'fabricante': fabricante,
                'capacidad': capacidad,
                'rango': rango
            }
        )

        return {
            'statusCode': 201,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({'message': 'Avión creado con éxito'})
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({'message': 'Error al crear el avión', 'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({'message': 'Error desconocido', 'error': str(e)})
        }

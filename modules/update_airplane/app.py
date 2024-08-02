import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('planes-new')  # Nombre de tabla actualizado

def lambda_handler(event, context):
    try:
        # Parse the request body
        data = json.loads(event['body'])

        # Validate fields
        id = data.get('id')
        modelo = data.get('modelo')
        fabricante = data.get('fabricante')
        capacidad = data.get('capacidad')
        rango = data.get('rango')

        if not id or not isinstance(id, str):
            raise ValueError('El campo "id" es requerido y debe ser una cadena.')
        if not modelo or not isinstance(modelo, str):
            raise ValueError('El campo "modelo" es requerido y debe ser una cadena.')
        if not fabricante or not isinstance(fabricante, str):
            raise ValueError('El campo "fabricante" es requerido y debe ser una cadena.')
        if not capacidad or not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError('El campo "capacidad" es requerido y debe ser un entero positivo.')

        # Check if the item exists in DynamoDB
        response = table.get_item(Key={'id': id})
        if 'Item' not in response:
            raise ValueError(f'El avión con id "{id}" no existe.')

        # Update item in DynamoDB
        table.update_item(
            Key={'id': id},
            UpdateExpression='SET modelo = :modelo, fabricante = :fabricante, capacidad = :capacidad, rango = :rango',
            ExpressionAttributeValues={
                ':modelo': modelo,
                ':fabricante': fabricante,
                ':capacidad': capacidad,
                ':rango': rango
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({'message': 'Avión actualizado exitosamente!'})
        }

    except ValueError as ve:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({'error': str(ve)})
        }
    except ClientError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({'error': f'Error inesperado: {str(e)}'})
        }

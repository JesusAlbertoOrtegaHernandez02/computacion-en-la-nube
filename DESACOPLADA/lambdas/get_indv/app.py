import json
import os
import boto3
from botocore.exceptions import ClientError

# Conexión a DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table_name = os.getenv("DYNAMO_TABLE", "products")
table = dynamodb.Table(table_name)


def get_item(item_id):
    """Obtiene un ítem por su ID desde DynamoDB."""
    try:
        response = table.get_item(Key={"id": item_id})
        return response.get("Item")
    except ClientError as e:
        return {"error": str(e)}


def lambda_handler(event, context):
    try:
        # Obtenemos el ID desde pathParameters
        item_id = event["pathParameters"]["id"]
        result = get_item(item_id)

        # Si no se encontró el ítem
        if not result or "error" in result:
            return {
                "statusCode": 404,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps(
                    {"error": f"Elemento con id '{item_id}' no encontrado"}
                )
            }

        # Si todo va bien
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(result, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }

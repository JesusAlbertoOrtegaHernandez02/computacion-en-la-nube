import json
import os
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table_name = os.getenv("DYNAMO_TABLE", "products")
table = dynamodb.Table(table_name)

def delete_item(item_id):
    """Elimina un ítem del DynamoDB por su id"""
    try:
        table.delete_item(Key={"id": item_id})
        return {"message": "Item eliminado correctamente"}
    except ClientError as e:
        return {"error": str(e)}

def lambda_handler(event, context):
    """Lambda principal"""
    try:
        item_id = event["pathParameters"]["id"]
        result = delete_item(item_id)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }

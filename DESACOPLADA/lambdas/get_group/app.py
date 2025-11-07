import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table_name = os.getenv("DYNAMO_TABLE", "products")
table = dynamodb.Table(table_name)


def get_all_items():
    """Obtiene todos los items de la tabla DynamoDB."""
    try:
        response = table.scan()
        items = response.get("Items", [])

        if not items:
            return {
                "message": "No se encontraron ítems en la tabla.",
                "count": 0,
                "items": []
            }

        return {
            "message": f"Se encontraron {len(items)} ítems.",
            "count": len(items),
            "items": items
        }

    except ClientError as e:
        return {"error": str(e)}


def lambda_handler(event, context):
    """Manejador principal de la Lambda"""
    try:
        result = get_all_items()

        if "error" in result:
            status_code = 500
        elif result.get("count", 0) == 0:
            status_code = 404
        else:
            status_code = 200

        return {
            "statusCode": status_code,
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

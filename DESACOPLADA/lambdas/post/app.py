import json
import os
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table_name = os.getenv("DYNAMO_TABLE", "products")
table = dynamodb.Table(table_name)


def convert_numbers(data):
    """Convierte floats a Decimal (requisito de DynamoDB)."""
    for k, v in data.items():
        if isinstance(v, float):
            data[k] = Decimal(str(v))
        elif isinstance(v, dict):
            convert_numbers(v)
    return data


def create_item(item):
    """Inserta un nuevo ítem en DynamoDB."""
    try:
        item = convert_numbers(item)
        table.put_item(Item=item)
        return {"message": "Item creado correctamente", "item": item}
    except ClientError as e:
        return {"error": str(e)}


def lambda_handler(event, context):
    """Manejador principal de la Lambda."""
    try:
        body = json.loads(event["body"])
        result = create_item(body)

        return {
            "statusCode": 200 if "error" not in result else 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
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

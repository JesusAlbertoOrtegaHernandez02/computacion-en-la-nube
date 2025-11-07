import json
import os
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table_name = os.getenv("DYNAMO_TABLE", "products")
table = dynamodb.Table(table_name)


def convert_numbers(data):
    for k, v in data.items():
        if isinstance(v, float):
            data[k] = Decimal(str(v))
        elif isinstance(v, dict):
            convert_numbers(v)
    return data


def update_item(item_id, data):
    """Actualiza un ítem en DynamoDB por su ID."""
    try:
        data = convert_numbers(data)
        update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in data.keys())
        expression_attr_names = {f"#{k}": k for k in data.keys()}
        expression_attr_values = {f":{k}": v for k, v in data.items()}

        response = table.update_item(
            Key={"id": item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attr_names,
            ExpressionAttributeValues=expression_attr_values,
            ReturnValues="ALL_NEW"
        )
        return {
            "message": f"Item {item_id} actualizado correctamente",
            "attributes": response.get("Attributes", {})
        }

    except ClientError as e:
        return {"error": str(e)}


def lambda_handler(event, context):
    try:
        item_id = event["pathParameters"]["id"]
        body = json.loads(event["body"])
        result = update_item(item_id, body)

        return {
            "statusCode": 200 if "error" not in result else 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "PUT,OPTIONS",
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

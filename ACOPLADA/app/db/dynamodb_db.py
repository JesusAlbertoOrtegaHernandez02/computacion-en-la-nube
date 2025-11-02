from decimal import Decimal
import boto3
from botocore.exceptions import ClientError
import os

class DynamoDB:
    def __init__(self):
        self.table_name = os.getenv("DYNAMO_TABLE", "products")
        self.dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        self.table = self.dynamodb.Table(self.table_name)

    def _convert_numbers(self, data):
        for k, v in data.items():
            if isinstance(v, float):
                data[k] = Decimal(str(v))
            elif isinstance(v, dict):
                self._convert_numbers(v)
        return data

    def create_item(self, item):
        try:
            item = self._convert_numbers(item)
            self.table.put_item(Item=item)
            return {"message": "Item creado correctamente", "item": item}
        except ClientError as e:
            return {"error": str(e)}

    def get_item(self, item_id):
        try:
            response = self.table.get_item(Key={"id": item_id})
            return response.get("Item")
        except ClientError as e:
            return {"error": str(e)}

    def get_all_items(self):
        try:
            response = self.table.scan()
            return response.get("Items", [])
        except ClientError as e:
            return {"error": str(e)}

    def update_item(self, item_id, data):
        data = self._convert_numbers(data)
        update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in data.keys())
        expression_attr_names = {f"#{k}": k for k in data.keys()}
        expression_attr_values = {f":{k}": v for k, v in data.items()}

        try:
            response = self.table.update_item(
                Key={"id": item_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attr_names,
                ExpressionAttributeValues=expression_attr_values,
                ReturnValues="ALL_NEW"
            )
            return response.get("Attributes", {})
        except ClientError as e:
            return {"error": str(e)}

    def delete_item(self, item_id):
        try:
            self.table.delete_item(Key={"id": item_id})
            return {"message": "Item eliminado correctamente"}
        except ClientError as e:
            return {"error": str(e)}

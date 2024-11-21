import boto3
import json
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VehiclesTable')

def create_vehicle(event, context):
    data = json.loads(event['body'])
    item = {
        'id': str(uuid4()),
        'model': data['model'],
        'status': data.get('status', 'active')
    }
    table.put_item(Item=item)
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Vehicle created", "vehicle": item})
    }

def get_vehicles(event, context):
    response = table.scan()
    return {
        "statusCode": 200,
        "body": json.dumps(response['Items'])
    }

def update_vehicle(event, context):
    vehicle_id = event['pathParameters']['id']
    data = json.loads(event['body'])
    update_expression = "SET"
    expression_attribute_values = {}

    for key, value in data.items():
        update_expression += f"{key} = :{key}, "
        expression_attribute_values[f":{key}"] = value

    update_expression = update_expression.rstrip(", ")

    table.update_item(
        Key={'id': vehicle_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Vehicle updated"})
    }

def log_updates(event, context):
    for record in event['Records']:
        if record['eventName'] == 'MODIFY':
            print(f"Update vehicle {record['dynamodb']['NewItem']}")
    return {"statusCode": 200}


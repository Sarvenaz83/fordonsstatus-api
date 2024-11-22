import boto3
import json
import logging
from uuid import uuid4

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VehiclesTable')

# Create a new vehicle
def create_vehicle(event, context):
    try:
        data = json.loads(event['body'])
        item = {
            'id': str(uuid4()),
            'model': data['model'],
            'status': data.get('status', 'active')  # Default status is 'active'
        }
        table.put_item(Item=item)
        logger.info(f"Vehicle created: {item}")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Vehicle created", "vehicle": item})
        }
    except Exception as e:
        logger.error(f"Error creating vehicle: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# Retrieve all vehicles with pagination
def get_vehicles(event, context):
    try:
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 10))
        response = table.scan(Limit=limit)
        return {
            "statusCode": 200,
            "body": json.dumps(response.get('Items', []))
        }
    except Exception as e:
        logger.error(f"Error fetching vehicles: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# Retrieve a specific vehicle by ID
def get_vehicle_by_id(event, context):
    vehicle_id = event['pathParameters']['id']
    try:
        response = table.get_item(Key={'id': vehicle_id})
        if 'Item' in response:
            return {
                "statusCode": 200,
                "body": json.dumps(response['Item'])
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Vehicle not found"})
            }
    except Exception as e:
        logger.error(f"Error fetching vehicle: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# Update a vehicle's status
def update_vehicle(event, context):
    vehicle_id = event['pathParameters']['id']
    data = json.loads(event['body'])
    update_expression = "SET "
    expression_attribute_values = {}

    for key, value in data.items():
        update_expression += f"{key} = :{key}, "
        expression_attribute_values[f":{key}"] = value

    update_expression = update_expression.rstrip(", ")

    try:
        table.update_item(
            Key={'id': vehicle_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        logger.info(f"Vehicle {vehicle_id} updated: {data}")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Vehicle updated"})
        }
    except Exception as e:
        logger.error(f"Error updating vehicle: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# Log updates to vehicles via DynamoDB streams
def log_updates(event, context):
    for record in event['Records']:
        if record['eventName'] == 'MODIFY':
            new_image = record['dynamodb']['NewImage']
            old_image = record['dynamodb']['OldImage']
            logger.info(f"Vehicle updated: {new_image}, Previous state: {old_image}")
    return {"statusCode": 200}

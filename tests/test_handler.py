import json
import pytest
from unittest.mock import patch
from src.handler import create_vehicle, get_vehicles, get_vehicle_by_id


# Mock DynamoDB
from moto import mock_dynamodb
import boto3

import uuid

@mock_dynamodb
@pytest.fixture
def setup_dynamodb():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table_name = "VehiclesTable"

    # Ensure no existing table with the same name
    try:
        table = dynamodb.Table(table_name)
        table.delete()
        table.meta.client.get_waiter("table_not_exists").wait(TableName=table_name)
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        pass

    # Create the table
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
    yield table


def test_create_vehicle(setup_dynamodb):
    """Test the create_vehicle Lambda function."""
    # Test event
    event = {
        "body": json.dumps({"model": "Volvo xc90", "status": "active"})
    }
    context = {}

    # Call the function
    response = create_vehicle(event, context)

    # Assertions
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Vehicle created"
    assert body["vehicle"]["model"] == "Volvo xc90"


def test_get_vehicles(setup_dynamodb):
    table = setup_dynamodb
    table.put_item(Item={"id": "1", "model": "Volvo XC60", "status": "active"})

    event = {"queryStringParameters": {"limit": "10"}}
    context = {}
    response = get_vehicles(event, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert len(body) == 1
    assert body[0]["model"] == "Volvo XC60"


def test_get_vehicle_by_id(setup_dynamodb):
    table = setup_dynamodb
    table.put_item(Item={"id": "123", "model": "Volvo XC40", "status": "active"})

    event = {"pathParameters": {"id": "123"}}
    context = {}
    response = get_vehicle_by_id(event, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["model"] == "Volvo XC40"

Fordonsstatus API
A serverless application that provides an API for managing vehicle data. This project uses AWS Lambda, DynamoDB, and API Gateway.

API Endpoints
POST /vehicles
Creates a new vehicle record.

GET /vehicles
Retrieves a list of all vehicles.

GET /vehicle/{id}
Retrieves details of a vehicle by its id.

PATCH /vehicles/{id}
Updates a vehicle record.

Request/Response Examples
1. Create a Vehicle
Request:

POST /vehicles
Content-Type: application/json

{
  "model": "Volvo XC60",
  "status": "active"
}
Response:

{
  "message": "Vehicle created successfully",
  "id": "1234-5678-91011"
}
2. Get All Vehicles
Request:

GET /vehicles
Response:

[
  {
    "id": "1234-5678-91011",
    "model": "Volvo XC60",
    "status": "active"
  }
]
3. Get a Vehicle by ID
Request:

GET /vehicle/1234-5678-91011
Response:

{
  "id": "1234-5678-91011",
  "model": "Volvo XC60",
  "status": "active"
}
4. Update a Vehicle
Request:

PATCH /vehicles/1234-5678-91011
Content-Type: application/json

{
  "status": "inactive"
}
Response:

{
  "message": "Vehicle updated successfully"
}
Running Tests Locally
1. Prerequisites
Python 3.7 or higher
Node.js
Virtual environment tool (venv or virtualenv)
2. Setup Instructions
Clone the repository:

git clone https://github.com/Sarvenaz83/fordonsstatus-api.git
cd fordonsstatus-api
Set up a virtual environment:

python -m venv venv
source venv/bin/activate  # For Windows: .\venv\Scripts\activate
Install Python dependencies:

pip install -r requirements.txt
Install Node.js dependencies:

npm install
3. Run Tests
To execute the unit tests:

pytest tests/
Expected Output: All tests should pass with output like:

tests/test_handler.py ...                                                                                             [100%]

============================================== 3 passed in 106.59s (0:01:46) ===============================================
Deployment
Deploy the application to AWS using Serverless Framework:

serverless deploy
Output: You will see the API Gateway endpoint in the output. Use it to access your endpoints.

Project Structure
fordonsstatus-api/
│
├── handler.py               # Lambda functions for the API
├── serverless.yml           # Serverless Framework configuration
├── tests/
│   ├── test_handler.py      # Unit tests for the Lambda functions
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
├── package.json             # Node.js dependencies
└── README.md                # Project documentation
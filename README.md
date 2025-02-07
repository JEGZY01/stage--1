Number Classifier API
This FastAPI application provides an API to classify numbers based on various mathematical properties. The API includes endpoints to check if a number is prime, perfect, an Armstrong number, even/odd, and also provides a fun fact related to the number.

Features
Prime Check: Classify whether a number is prime.
Perfect Number Check: Determine if the number is a perfect number.
Armstrong Number Check: Check if a number is an Armstrong number.
Odd/Even Check: Classify a number as odd or even.
Digit Sum: Get the sum of the digits of the number.
Fun Fact: Retrieve a fun fact about the number from an external service.
Installation
Clone the repository:

bash
Copy
Edit
git clone <repository_url>
cd <repository_directory>
Set up a virtual environment:

bash
Copy
Edit
python -m venv .venv
Activate the virtual environment:

Windows:
bash
Copy
Edit
.venv\Scripts\activate
macOS/Linux:
bash
Copy
Edit
source .venv/bin/activate
Install the required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
The requirements.txt should include:

nginx
Copy
Edit
fastapi
uvicorn
requests
Running the Application
To start the API server, run the following command:

bash
Copy
Edit
uvicorn main:app --reload
This will start the server at http://127.0.0.1:8000.

API Endpoints
Classify a number

URL: /api/classify-number

Method: GET

Query Parameter:

number: The number you want to classify (integer).
Response:

is_prime: Boolean indicating whether the number is prime.
is_perfect: Boolean indicating whether the number is perfect.
properties: List of properties the number has (e.g., Armstrong, even/odd).
digit_sum: Sum of the digits of the number.
fun_fact: A fun fact about the number retrieved from the Numbers API.
Example Request:

nginx
Copy
Edit
GET http://127.0.0.1:8000/api/classify-number?number=28
Example Response:

json
Copy
Edit
{
    "number": 28,
    "is_prime": false,
    "is_perfect": true,
    "properties": ["even"],
    "digit_sum": 10,
    "fun_fact": "28 is a perfect number."
}
Testing the API
You can test the API using tools like Postman or cURL by sending GET requests to http://127.0.0.1:8000/api/classify-number?number=<your_number>.
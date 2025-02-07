from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi.responses import JSONResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_prime(number):
    prime = True
    for n in range(2, number):
        if number % n == 0:
            prime = False
    return prime

def is_perfect(number):
    perfect = False
    division_sum = 0
    for n in range(1, number):
        if number % n == 0:
            division_sum += n
    if division_sum == number:
        perfect = True

    return perfect

def digit_sum(number):
    total = 0
    for digit in str(abs(number)):  # Convert number to a string to iterate over digits
        total += int(digit)
    return total

def properties(number):
    number_properties = []

    # Check if Armstrong
    armstrong_sum = sum(int(digit) ** len(str(number)) for digit in str(number))
    if armstrong_sum == number:
        number_properties.append("armstrong")

    # Check odd or even
    if number % 2 == 0:
        number_properties.append("even")
    else:
        number_properties.append("odd")

    return number_properties

def fun_fact(number: int) -> str|None:
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math")
        return response.text if response.ok else "No fun fact available."
    except:
        return None

@app.get("/api/classify-number",status_code=200)
def classify_number(number: int|str|None=None):
    # Check for valid input
    if number is None:
        return JSONResponse({
            "number":"Pls provide a number in query param",
            "error":True,
        },status_code=400, )
    try:
        int(number)
    except ValueError:
        # Handle non-numeric inputs
        return JSONResponse({"number": "alphabet", "error": True}, status_code=400)
    if number < 0:
        return JSONResponse({"number": "negative integer", "error": True}, status_code=400)
    if str(number).replace('.', '', 1).isdigit() and '.' in str(number):
        return JSONResponse(
            {"number": "float", "error": True}, status_code=400
        )


        # Check for float input
    if not isinstance(number, int):
        return JSONResponse({"number":type(number),"error":True},status_code=400)

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties(number),
        "digit_sum": digit_sum(number),
        "fun_fact": fun_fact(number) or "No fun fact available",
    }


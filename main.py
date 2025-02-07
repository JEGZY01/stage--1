from fastapi import FastAPI, HTTPException,status,params
from fastapi.middleware.cors import CORSMiddleware
import requests


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

def fun_fact(number: int) -> str:
    response = requests.get(f"http://numbersapi.com/{number}/math")
    return response.text if response.ok else "No fun fact available."

@app.get("/api/classify-number",status_code=200)
def classify_number(number: int|None=None):
    # Check for valid input
    if not number:
        raise HTTPException(status_code=400, detail="Please provide a number.")
    if not isinstance(number, int):
        raise HTTPException(status_code=400, detail="Invalid input. Please provide a number.")
    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties(number),
        "digit_sum": digit_sum(number),
        "fun_fact": fun_fact(number),
    }


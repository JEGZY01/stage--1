from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import requests


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#
#
# def is_prime(number):
#     prime = True
#     for n in range(2, number):
#         if number % n == 0:
#             prime = False
#     return prime
#
# def is_perfect(number):
#     perfect = False
#     division_sum = 0
#     for n in range(1, number):
#         if number % n == 0:
#             division_sum += n
#     if division_sum == number:
#         perfect = True
#
#     return perfect
#
# def digit_sum(number):
#     total = 0
#     for digit in str(abs(number)):  # Convert number to a string to iterate over digits
#         total += int(digit)
#     return total
#
# def properties(number):
#     number_properties = []
#
#     # Check if Armstrong
#     armstrong_sum = sum(int(digit) ** len(str(number)) for digit in str(number))
#     if armstrong_sum == number:
#         number_properties.append("armstrong")
#
#     # Check odd or even
#     if number % 2 == 0:
#         number_properties.append("even")
#     else:
#         number_properties.append("odd")
#
#     return number_properties
#
# def fun_fact(number: int) -> str|None:
#     try:
#         response = requests.get(f"http://numbersapi.com/{number}/math")
#         return response.text if response.ok else "No fun fact available."
#     except:
#         return None
#
# @app.get("/api/classify-number",status_code=200)
# def classify_number(number: int|str|None=None):
#     # Check for valid input
#     if number is None:
#         return JSONResponse({
#             "number":"Pls provide a number in query param",
#             "error":True,
#         },status_code=400, )
#     try:
#         int(number)
#     except ValueError:
#         # Handle non-numeric inputs
#         return JSONResponse({"number": "alphabet", "error": True}, status_code=400)
#     if number < 0:
#         return JSONResponse({"number": "negative integer", "error": True}, status_code=400)
#     if str(number).replace('.', '', 1).isdigit() and '.' in str(number):
#         return JSONResponse(
#             {"number": "float", "error": True}, status_code=400
#         )
#
#
#         # Check for float input
#     if not isinstance(number, int):
#         return JSONResponse({"number":type(number),"error":True},status_code=400)
#
#     return {
#         "number": number,
#         "is_prime": is_prime(number),
#         "is_perfect": is_perfect(number),
#         "properties": properties(number),
#         "digit_sum": digit_sum(number),
#         "fun_fact": fun_fact(number) or "No fun fact available",
#     }
#




class NumberService:
    async def get_is_prime(self, number):
        if number < 0 or number == 0 or number == 1:
            return False
        for i in range(2, number):
            if (number % i) == 0:
                # If a factor is found, then number is not a prime number
                return False
        return True

    async def get_is_perfect(self, number):
        if number < 0:
            return False
        sum = 0
        for i in range(1, number):
            if number % i == 0:
                sum += i
        return number == sum

    async def get_is_armstrong(self, number):
        if number < 0:
            return False
        order = len(str(number))
        sum = 0
        temp = number
        while temp > 0:
            digit = temp % 10
            sum += digit ** order
            temp //= 10
        return sum == number

    async def get_digit_sum(self, number):
        number = abs(number)
        return sum(list(map(int, str(number))))

    async def get_is_odd(self, number):
        if number % 2 == 0:
            return False
        return True

    async def get_properties(self, number):
        property = []
        if await self.get_is_armstrong(number):
            property.append("armstrong")
        if await self.get_is_odd(number):
            property.append("odd")
            return property
        property.append("even")
        return property

    async def get_fun_fact(self, number):
        api_url = f"http://numbersapi.com/{number}/math?json"

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raises an error for HTTP errors
            return response.json()["text"] if "text" in response.json() else "No text found"
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

number_service = NumberService()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    query_parameter = request.query_params._dict["number"]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        # content=jsonable_encoder({"detail": exc.errors(),  # optionally include the errors
        #         "body": exc.body,
        #          "custom msg": {"Your error message"}}),
        content={
            "number": query_parameter,
            "error": True
        },
    )


@app.get('/api/classify-number')
async def number_class(number: int):
    try:
        fun_fact = await number_service.get_fun_fact(number)
        is_prime = await number_service.get_is_prime(number)
        is_perfect = await number_service.get_is_perfect(number)
        properties = await number_service.get_properties(number)
        digit_sum = await number_service.get_digit_sum(number)
        return JSONResponse(
            content={
                "number": number,
                "is_prime": is_prime,
                "is_perfect": is_perfect,
                "properties": properties,
                "digit_sum": digit_sum,
                "fun_fact": fun_fact
            },
            status_code=status.HTTP_200_OK
        )
    except Exception:
        return JSONResponse(
            content={
                "msg": "something went wrong",
                "error": True
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )


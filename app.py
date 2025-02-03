from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.json.sort_keys = False

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    sum_divisors = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors == n

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]  # Use absolute value to handle negative numbers
    num_digits = len(digits)
    return sum(d ** num_digits for d in digits) == abs(n)  # Compare with absolute value

def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math")
    return response.text if response.status_code == 200 else "No fun fact available"

@app.route('/')
def home():
    return '<h1> Welcome! Try GET /api/classify-number?number={your choice} </h1>'

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    # Handle negative numbers and non-digit inputs
    try:
        number = int(number)  # Convert to integer (handles negative numbers)
    except (ValueError, TypeError):
        return jsonify({"number": number, "error": True}), 400
    
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    digit_sum = sum(int(d) for d in str(abs(number)))  # Use absolute value for digit sum
    fun_fact = get_fun_fact(number)

    return jsonify({
        "number": number,
        "is_prime": is_prime(abs(number)),  # Use absolute value for prime check
        "is_perfect": is_perfect(abs(number)),  # Use absolute value for perfect check
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

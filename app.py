import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import stripe
from waitress import serve

# Load secret keys from your .env file and support both uppercase/lowercase variations
load_dotenv()
stripe_key = os.getenv("STRIPE_SECRET_KEY") or os.getenv("stripe_secret_key")

if not stripe_key:
    raise ValueError("CRITICAL ERROR: Stripe secret key not found in .env file!")

stripe.api_key = stripe_key

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        cart_items = data.get('cart', [])
        
        if not cart_items:
            return jsonify(error="Cart is empty"), 400

        line_items = []
        for item in cart_items:
            unit_amount_cents = int(float(item['price']) * 100)
            
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['name'],
                    },
                    'unit_amount': unit_amount_cents,
                },
                'quantity': item['quantity'],
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://simplesourdough4u.com/success.html',
            cancel_url='https://simplesourdough4u.com/cancel.html',
        )
        return jsonify({'url': checkout_session.url})
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    print("Starting production server with Waitress on port 5000...")
    serve(app, host='0.0.0.0', port=5000)
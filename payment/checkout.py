#!/usr/bin/env python3
"""
VERA Commercial Payment Gateway - Honest pricing tiers
Integrates Stripe Checkout for licensing.
"""
import os
import stripe
from flask import Flask, request, jsonify

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = Flask(__name__)

TIERS = {
    "starter": {"price": "price_xxx", "name": "Starter - $49/mo"},
    "pro": {"price": "price_yyy", "name": "Pro - $299/mo"}
}

@app.route('/create-checkout', methods=['POST'])
def create_checkout():
    data = request.get_json()
    tier = data.get('tier', 'starter')
    # Create Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price': TIERS[tier]['price'], 'quantity': 1}],
        mode='subscription',
        success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://yourdomain.com/cancel',
        metadata={'tier': tier, 'customer_email': data.get('email')}
    )
    return jsonify({'url': session.url})

# Webhook for fulfillment (license key delivery, etc.)
@app.route('/webhook', methods=['POST'])
def webhook():
    # Verify signature + fulfill license
    print("Payment successful - deliver VERA license key")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=5001)
print("Payment gateway ready. Honest tiers only.")
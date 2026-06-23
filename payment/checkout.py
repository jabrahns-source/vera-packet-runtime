#!/usr/bin/env python3
"""
VERA Commercial Payment Gateway - Honest pricing tiers
Integrates Stripe Checkout for licensing.
Replace PRICE_ID_xxx with actual IDs from your Stripe Dashboard after creating products.
"""
import os
import stripe
from flask import Flask, request, jsonify

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = Flask(__name__)

# TODO: Create these Price IDs in Stripe Dashboard (Products → Prices)
# Starter: monthly $49, Pro: monthly $299
TIERS = {
    "starter": {
        "price_id": "price_1XXXXXXXXXXXXXXXXXXXXXXXXX",  # Replace with real Starter price ID
        "name": "Starter - $49/mo"
    },
    "pro": {
        "price_id": "price_1XXXXXXXXXXXXXXXXXXXXXXXXX",  # Replace with real Pro price ID
        "name": "Pro - $299/mo"
    }
}

@app.route('/create-checkout', methods=['POST'])
def create_checkout():
    data = request.get_json()
    tier = data.get('tier', 'starter')
    tier_config = TIERS.get(tier)
    if not tier_config:
        return jsonify({'error': 'Invalid tier'}), 400
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price': tier_config['price_id'], 'quantity': 1}],
        mode='subscription',
        success_url=os.getenv('SUCCESS_URL', 'https://your-vera-domain.com/success?session_id={CHECKOUT_SESSION_ID}'),
        cancel_url=os.getenv('CANCEL_URL', 'https://your-vera-domain.com/cancel'),
        metadata={
            'tier': tier,
            'customer_email': data.get('email'),
            'customer_name': data.get('name', 'VERA User')
        }
    )
    return jsonify({'url': session.url})

# Webhook for fulfillment (license key generation + delivery)
@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # TODO: Generate license key, email it, activate access
        print(f"[PAYMENT] Success for {session.get('customer_email')} - Tier: {session.get('metadata', {}).get('tier')}")
        # Integrate with VERA license check here
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    print("VERA Payment Gateway running on port 5001")
    print("Set STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, SUCCESS_URL in .env")
    app.run(port=5001, debug=False)

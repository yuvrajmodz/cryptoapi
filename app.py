from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

# Developed By YuvrajMODZ

# Function to scrape data for a specific cryptocurrency
def scrape_crypto_data(crypto_code):
    url = 'https://crypto.com/price'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table row containing the requested cryptocurrency
    rows = soup.find_all('tr', class_='css-1cxc880')

    for row in rows:
        # Find the short code (like BTC, ETH) in the row
        code_tag = row.find('span', class_='chakra-text css-1jj7b1a')
        
        if code_tag and code_tag.text.strip().lower() == crypto_code.lower():
            name_tag = row.find('p', class_='chakra-text css-rkws3')
            price_tag = row.find('p', class_='chakra-text css-13hqrwd')
            market_cap_tag = row.find_all('td', class_='css-15lyn3l')
            
            if name_tag and price_tag and market_cap_tag:
                name = name_tag.text.strip()
                price = price_tag.text.strip()
                market_cap = market_cap_tag[1].text.strip()

                # Return the data in the correct order
                return {
                    'name': name,
                    'symbol': code_tag.text.strip(),
                    'price': price,
                    'market_cap': market_cap
                }
    return None

# API endpoint to get data for a specific cryptocurrency
@app.route('/crypto-api', methods=['GET'])
def get_crypto_data():
    crypto_code = request.args.get('cr')  # Get the 'cr' parameter from the query string
    
    if not crypto_code:
        return jsonify({'error': 'Please provide a valid cryptocurrency code.'}), 400

    data = scrape_crypto_data(crypto_code)
    
    if data:
        # Use json.dumps to ensure the correct order of keys
        ordered_data = json.dumps(data, indent=4)  # indented for better readability
        return ordered_data, 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({'error': f'Cryptocurrency with code {crypto_code} not found.'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
# midri_mcro_module.py
from flask import Blueprint, request, jsonify
from datetime import datetime
import urllib.parse

midri_mcro = Blueprint('midri_mcro', __name__)

@midri_mcro.route('/api/midri/mcro_eviction_search', methods=['POST'])
def mcro_eviction_search():
    data = request.get_json()
    search_term = data.get('search_term', '').strip()

    if not search_term:
        return jsonify({'error': 'Missing search term'}), 400

    encoded_term = urllib.parse.quote_plus(search_term)
    search_url = f"https://publicaccess.courts.state.mn.us/MCRO/CaseSearch?SearchTerm={encoded_term}"

    log = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'search_term': search_term,
        'search_url': search_url,
        'status': 'launched'
    }

    return jsonify(log), 200
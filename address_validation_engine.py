import os
import requests

class AddressValidationResult:
    def __init__(self, validated=False, confidence=0.0, normalized=None, lat=None, lon=None, provider="nominatim", raw=None, suggestions=None):
        self.validated = validated
        self.confidence = confidence
        self.normalized = normalized or {}
        self.lat = lat
        self.lon = lon
        self.provider = provider
        self.raw = raw or {}
        self.suggestions = suggestions or []

    def to_dict(self):
        return {
            'validated': self.validated,
            'confidence': self.confidence,
            'normalized': self.normalized,
            'lat': self.lat,
            'lon': self.lon,
            'provider': self.provider,
            'raw': self.raw,
            'suggestions': self.suggestions,
        }

def _nominatim_headers():
    email = os.environ.get('NOMINATIM_EMAIL', 'semptify@example.com')
    return { 'User-Agent': f'Semptify/1.0 (+{email})' }


def validate_and_enrich_address(address, city, state, zip_code, country='US'):
    """Validate and normalize an address using OpenStreetMap Nominatim.
    Falls back gracefully if network is unavailable. Returns AddressValidationResult.
    """
    base_url = os.environ.get('NOMINATIM_BASE_URL', 'https://nominatim.openstreetmap.org')
    try:
        q = f"{address}, {city}, {state} {zip_code}, {country}"
        params = { 'q': q, 'format': 'jsonv2', 'addressdetails': 1, 'limit': 3 }
        r = requests.get(f"{base_url}/search", params=params, headers=_nominatim_headers(), timeout=8)
        r.raise_for_status()
        results = r.json() or []
        if not results:
            return AddressValidationResult(validated=False, confidence=0.0, suggestions=[])
        best = results[0]
        addr = best.get('address', {})
        normalized = {
            'address': f"{addr.get('house_number', '')} {addr.get('road', '')}".strip(),
            'city': addr.get('city') or addr.get('town') or addr.get('village') or addr.get('hamlet') or city,
            'state': addr.get('state') or state,
            'zip': addr.get('postcode') or zip_code,
            'country': addr.get('country_code','').upper() or country,
            'display_name': best.get('display_name'),
        }
        conf = 0.8
        if addr.get('postcode') == zip_code:
            conf += 0.1
        if state.lower() in (addr.get('state','').lower()):
            conf += 0.05
        return AddressValidationResult(
            validated=True,
            confidence=min(conf, 0.99),
            normalized=normalized,
            lat=float(best.get('lat')),
            lon=float(best.get('lon')),
            provider='nominatim',
            raw=best,
            suggestions=[r.get('display_name') for r in results]
        )
    except Exception:
        return AddressValidationResult(validated=False, confidence=0.0)

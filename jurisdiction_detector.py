from typing import Dict, Any, List
import re

STATE_ABBR = {
    'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming'
}

AREA_CODE_HINTS = {
    # Very small seed set; low confidence hints
    'MN': {'612','651','763','952','218','320','507'},
    'CA': {'415','510','650','408','213','310','424','619','760','818'},
    'TX': {'214','469','972','817','682','512','737','713','281','832'},
    'NY': {'212','315','332','347','516','518','585','607','631','646','716','718','845','914','917','929','934'}
}

CITY_HINTS = {
    'MN': {'minneapolis','saint paul','st. paul','duluth','rochester','bloomington','eden prairie'},
    'CA': {'los angeles','san francisco','oakland','san jose','san diego','fresno','sacramento'},
    'TX': {'dallas','austin','houston','san antonio','fort worth','el paso'},
    'NY': {'new york','brooklyn','queens','buffalo','rochester','syracuse','albany'}
}

STATE_NAMES = {v.lower():k for k,v in STATE_ABBR.items()}

WEIGHTS = {
    'text_state': 0.5,
    'text_city': 0.3,
    'doc_text': 0.4,
    'registration': 0.8,
    'area_code': 0.2,
    'ip_geo': 0.15,
}

STATE_LIST = set(STATE_ABBR.values())

STATE_REGEX = re.compile(r'\b(' + '|'.join([re.escape(name) for name in STATE_NAMES.keys()]) + r')\b', re.I)
ABBR_REGEX = re.compile(r'\b(' + '|'.join(STATE_ABBR.keys()) + r')\b')


def detect_jurisdiction(context: Dict[str, Any]) -> Dict[str, Any]:
    """Infer likely U.S. state from multiple weak/strong signals.
    context keys: text, doc_text, registration_state, phone, ip, headers
    Returns: { state, confidence, sources: [{type, value, weight}] }
    """
    signals: List[Dict[str, Any]] = []
    text = (context.get('text') or '').lower()
    doc_text = (context.get('doc_text') or '').lower()
    registration_state = context.get('registration_state')
    phone = context.get('phone') or ''

    # Registration (strong when present)
    if registration_state and registration_state.upper() in STATE_ABBR:
        st = registration_state.upper()
        signals.append({'type':'registration','value':st,'state':st,'weight':WEIGHTS['registration']})

    # Text explicit state names
    for m in STATE_REGEX.finditer(text):
        name = m.group(1).lower()
        st = STATE_NAMES.get(name)
        if st:
            signals.append({'type':'text_state','value':name,'state':st,'weight':WEIGHTS['text_state']})

    # Abbreviations like "MN", "CA"
    for m in ABBR_REGEX.finditer(text):
        st = m.group(1).upper()
        signals.append({'type':'text_state','value':st,'state':st,'weight':WEIGHTS['text_state']*0.7})

    # Cities
    for st, cities in CITY_HINTS.items():
        for city in cities:
            if city in text:
                signals.append({'type':'text_city','value':city,'state':st,'weight':WEIGHTS['text_city']})

    # Document text hints
    if doc_text:
        for m in STATE_REGEX.finditer(doc_text):
            name = m.group(1).lower()
            st = STATE_NAMES.get(name)
            if st:
                signals.append({'type':'doc_text','value':name,'state':st,'weight':WEIGHTS['doc_text']})

    # Phone area code (weak)
    m = re.match(r'\+?1?\D*(\d{3})', phone)
    if m:
        ac = m.group(1)
        for st, codes in AREA_CODE_HINTS.items():
            if ac in codes:
                signals.append({'type':'area_code','value':ac,'state':st,'weight':WEIGHTS['area_code']})

    # IP / headers (placeholder, low weight)
    ip = context.get('ip') or ''
    if ip:
        # Without external service, don't guess state; include as provenance only
        signals.append({'type':'ip_geo','value':ip,'state':None,'weight':WEIGHTS['ip_geo']})

    # Aggregate
    by_state: Dict[str, float] = {}
    for s in signals:
        st = s.get('state')
        if not st:
            continue
        by_state[st] = by_state.get(st, 0.0) + s['weight']

    if not by_state:
        return {'state': None, 'confidence': 0.0, 'sources': signals, 'explanation': 'No reliable jurisdiction signals found'}

    # Pick top state
    top_state, score = max(by_state.items(), key=lambda kv: kv[1])
    # Normalize confidence roughly to 0..1 with cap at 0.95
    max_possible = sum(WEIGHTS.values())
    confidence = min(0.95, score / max_possible)

    used_sources = [s for s in signals if s.get('state') == top_state]
    return {
        'state': top_state,
        'confidence': round(confidence, 2),
        'sources': used_sources,
        'explanation': f"Assumed {top_state} from signals: " + ', '.join(f"{s['type']}={s['value']}" for s in used_sources)
    }

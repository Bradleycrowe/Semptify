from flask import Blueprint, jsonify, request

evidence_meta = Blueprint('evidence_meta', __name__)

@evidence_meta.route('/evidence_metadata', methods=['GET','POST'])
def evidence_metadata():
    template = {
        'fields': [
            {'name':'filename','type':'string'},
            {'name':'uploaded_by','type':'string'},
            {'name':'timestamp_utc','type':'datetime'},
            {'name':'gps_lat','type':'number'},
            {'name':'gps_lon','type':'number'},
            {'name':'device_id','type':'string'},
            {'name':'description','type':'string'},
            {'name':'violation_tag','type':'string'},
            {'name':'chain_of_custody','type':'string'},
            {'name':'file_hash','type':'string'}
        ],
        'notes': 'Capture original file, hash, timestamp, uploader identity, and grouping tag.'
    }
    if request.method == 'POST':
        data = request.json or {}
        # TODO: validate and persist metadata
        return jsonify({'status':'ok','saved': data}), 201
    return jsonify(template)

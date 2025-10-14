from flask import Blueprint, render_template, request

evidence_packet_builder = Blueprint('evidence_packet_builder', __name__)

@evidence_packet_builder.route('/evidence_packet_builder')
def show_evidence_packet_builder():
    language = request.args.get('lang', 'en')
    content = {
        'en': {
            'title': 'Evidence Packet Builder',
            'sections': [
                {'heading':'Upload Evidence','text':'Attach photos, documents, audio, or video files that support your complaint.'},
                {'heading':'Organize by Violation','text':'Group evidence by issue: late fees, unsafe conditions, retaliation, or harassment.'},
                {'heading':'Export Packet','text':'Generate a printable, multilingual packet for regulators, attorneys, or court.'}
            ],
            'buttons': [
                {'label':'Upload Files','action':'/upload_evidence'},
                {'label':'Group by Violation','action':'/group_evidence'},
                {'label':'Export Packet','action':'/export_evidence_packet'},
                {'label':'Multilingual Export','action':'/export_multilingual'}
            ]
        }
    }
    return render_template('law_notes/law_notes_module.html', module=content.get(language, content['en']))

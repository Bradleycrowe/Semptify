from flask import Blueprint, render_template, request

attorney_trail = Blueprint('attorney_trail', __name__)

@attorney_trail.route('/attorney_trail')
def attorney_trail_view():
    lang = request.args.get('lang','en')
    content = {
        'en': {
            'title': 'Attorney Trail',
            'steps': [
                'Identify claims and jurisdiction',
                'Collect evidence packet',
                'Prepare retainer outline and jurisdiction-specific deadlines',
                'Draft cover memo for attorney review'
            ]
        }
    }
    return render_template('law_notes/attorney_trail.html', content=content.get(lang, content['en']))

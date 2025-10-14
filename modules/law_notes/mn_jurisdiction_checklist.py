from flask import Blueprint, render_template, request

mn_check = Blueprint('mn_check', __name__)

@mn_check.route('/mn_checklist')
def mn_checklist():
    address = request.args.get('address', '')
    language = request.args.get('lang', 'en')
    checklist = {
        'en': {
            'title': "Minnesota Jurisdiction Checklist",
            'state_statutes': [
                "Minn. Stat. Ch. 504B - Residential landlord and tenant",
                "Minn. Stat. Ch. 327A - Eviction procedure references",
                "Minn. Stat. Ch. 325F - Consumer protections where relevant"
            ],
            'local_actions': [
                "Check city rental licensing (Minneapolis, St. Paul)",
                "Lookup local code enforcement complaint process",
                "Confirm filing venue and service rules for housing court"
            ],
            'filing_steps': [
                "Record issue with dates and evidence",
                "Send demand letter per statute and local form",
                "File administrative complaint or small claims/civil filing as needed"
            ]
        }
    }
    return render_template('law_notes/jurisdiction_checklist.html', checklist=checklist.get(language, checklist['en']), address=address)

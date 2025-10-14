from flask import Blueprint, render_template, request

complaint_templates = Blueprint('complaint_templates', __name__)

@complaint_templates.route('/complaint_template')
def complaint_template():
    lang = request.args.get('lang', 'en')
    jurisdiction = request.args.get('jur', 'mn')
    templates = {
        'mn': {
            'late_fee': {
                'title': 'Late Fee Challenge - Minnesota',
                'citation': 'Minn. Stat. Ch. 504B; local ordinance',
                'body': 'Facts: [dates]; Legal basis: landlord failed to follow statutory notice and fee limits; Request: refund, correction, and penalty where applicable.'
            },
            'habitability': {
                'title': 'Habitability / Repair Demand - Minnesota',
                'citation': 'Minn. Stat. Ch. 504B; local housing code',
                'body': 'Facts: [dates]; Legal basis: landlord failed to maintain safe and sanitary premises; Request: repairs, rent abatement, administrative complaint.'
            }
        }
    }
    ttype = request.args.get('type','late_fee')
    tmpl = templates.get(jurisdiction, templates['mn']).get(ttype, templates['mn']['late_fee'])
    return render_template('law_notes/complaint_template.html', template=tmpl, lang=lang)

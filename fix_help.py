# Fix help_routes.py
with open('help_routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the index route to accept both with and without trailing slash
content = content.replace(
    "@help_bp.route('/', methods=['GET'])",
    "@help_bp.route('', methods=['GET'])"
)

# Remove the duplicate topic decorator on get_article
content = content.replace(
    "@help_bp.route('/topic/<topic_id>', methods=['GET'])\n@help_bp.route('/article/<article_id>', methods=['GET'])\ndef get_article(article_id):",
    "@help_bp.route('/article/<article_id>', methods=['GET'])\ndef get_article(article_id):"
)

with open('help_routes.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed help_routes.py')

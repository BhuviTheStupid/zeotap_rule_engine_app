from flask import Flask, request, jsonify, render_template
from database import fetch_rules, add_rule, get_all_rules, get_rules_by_ids
from rule_engine import create_rule, evaluate_rule

app = Flask(__name__)

# Route to display the index page with all rules
@app.route('/')
def index():
    try:
        # Fetch all rules to be displayed
        rules = fetch_rules()
        return render_template('index.html', rules=rules)
    except Exception as e:
        print(f"Error in Flask route: {e}")
        return "An error occurred", 500

@app.route('/evaluate', methods=['POST'])
def evaluate():
    json_data = request.get_json()

    if not json_data or 'rule_string' not in json_data or 'user_data' not in json_data:
        return jsonify({'error': 'Invalid input data'}), 400

    selected_rule_string = json_data['rule_string']
    user_data = json_data['user_data']

    ast = create_rule(selected_rule_string)

    if ast is None:
        return jsonify({'error': 'Invalid rule format'}), 400

    try:
        result = evaluate_rule(ast, user_data)
    except Exception as e:
        return jsonify({'error': f'Evaluation error: {str(e)}'}), 500

    return jsonify({'result': result})

@app.route('/add_rule', methods=['POST'])
def add_new_rule():
    rule_string = request.json.get('rule')
    add_rule(rule_string)
    return jsonify({'message': 'Rule added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    data = request.json
    rule_ids = data.get('rule_ids', [])
    operator = data.get('operator', 'AND')

    if not rule_ids or operator not in ['AND', 'OR']:
        return jsonify({'error': 'Invalid input'}), 400

    # Fetch the rules from the database
    rules = get_rules_by_ids(rule_ids)

    if not rules:
        return jsonify({'error': 'No rules found'}), 404

    # Combine rules using the selected operator
    combined_rule = f' {operator} '.join([rule['rule_string'] for rule in rules])

    return jsonify({'combined_rule': combined_rule})

# Endpoint to get rules
@app.route('/get_rules', methods=['GET'])
def get_rules():
    rules = get_all_rules()  # Assuming this function exists in database.py
    return jsonify({'rules': rules})

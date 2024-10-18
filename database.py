from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2024',
    'database': 'rule_engine'
}

# Function to fetch all rules from the database
def fetch_rules():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, rule FROM rules")
        rules = cursor.fetchall()
        return rules
    except mysql.connector.Error as err:
        print(f"Error fetching rules: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

# Function to combine rules
def combine_rules(rule_strings, operator):
    combined_rule = f" {' ' + operator + ' '}.join(rule_strings) "
    return combined_rule

# Save a new rule in the database
def add_rule(rule_string):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rules (rule) VALUES (%s)", (rule_string,))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    json_data = request.get_json()

    if not json_data or 'rule_ids' not in json_data or 'operator' not in json_data:
        return jsonify({'error': 'Invalid input data'}), 400

    rule_ids = json_data['rule_ids']
    operator = json_data['operator']

    # Fetch rules from the database based on the rule_ids
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT rule FROM rules WHERE id IN (%s)" % ','.join(['%s'] * len(rule_ids)), rule_ids)
    rules = cursor.fetchall()
    cursor.close()
    conn.close()

    # Combine the rules
    combined_rule = combine_rules([rule[0] for rule in rules], operator)

    # Save the combined rule
    add_rule(combined_rule)

    return jsonify({'combined_rule': combined_rule}), 201

# Function to get all rules from the database
def get_all_rules():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Return results as a dictionary
    cursor.execute("SELECT id, rule FROM rules")
    rules = cursor.fetchall()
    cursor.close()
    conn.close()
    return rules

# Function to get specific rules by their IDs
def get_rules_by_ids(rule_ids):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, rule FROM rules WHERE id IN (%s)" % ','.join(['%s'] * len(rule_ids))
    cursor.execute(query, rule_ids)
    rules = cursor.fetchall()
    cursor.close()
    conn.close()
    return rules
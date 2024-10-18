# zeotap_rule_engine_app
Here's a `README.md` file for your rule engine project that explains the structure, setup, usage, and key components.

---

# Rule Engine

## Overview

This Rule Engine is a Python-based application that allows you to create, combine, and evaluate logical rules based on user-defined conditions. The rules can be evaluated against a dataset provided as JSON, and they can be combined using logical operators such as `AND` and `OR`. The project uses Flask for the web interface and MySQL as the backend for storing the rules.

## Features

- **Create Rules**: Define new rules based on conditions such as `age > 30`.
- **Combine Rules**: Combine multiple rules using `AND` or `OR` operators.
- **Evaluate Rules**: Evaluate the rules against user data in JSON format.
- **Abstract Syntax Tree (AST)**: The rules are parsed into an AST for logical evaluation.
- **MySQL Database**: Store and retrieve rules from a MySQL database.

## Project Structure

```
.
├── app.py            # Main Flask application
├── database.py       # Database connection and query functions
├── rule_engine.py    # Logic for parsing and evaluating rules
├── models.py         # Node class definition for AST
├── templates/
│   └── index.html    # HTML template for the front-end
├── static/
│   └── styles.css    # CSS for styling the front-end
├── README.md         # Project documentation
└── requirements.txt  # List of required dependencies
```

## Getting Started

### Prerequisites

- **Python 3.x**
- **MySQL**: Make sure MySQL is installed and running.
- **Virtual Environment (optional)**: It's recommended to use a Python virtual environment for managing dependencies.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BhuviTheStupid/rule-engine.git
   cd rule-engine
   ```

2. **Install dependencies**:
   Use the provided `requirements.txt` file to install the required packages.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**:
   - Create a new database in MySQL:
     ```sql
     CREATE DATABASE rule_engine_db;
     ```
   - Create a table for storing rules:
     ```sql
     USE rule_engine_db;
     CREATE TABLE rules (
       id INT AUTO_INCREMENT PRIMARY KEY,
       rule_string TEXT NOT NULL
     );
     ```
   - Update the database configuration in `app.py` and `database.py`:
     ```python
     db_config = {
         'host': 'localhost',
         'user': 'your_username',
         'password': 'your_password',
         'database': 'rule_engine_db'
     }
     ```

4. **Run the Flask app**:
   Start the Flask development server.
   ```bash
   python app.py
   ```

   The app should now be running at `http://127.0.0.1:5000`.

## Usage

### Web Interface

1. **Access the Rule Engine**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

2. **Create a New Rule**:
   - Enter a rule in the form of conditions, e.g., `age > 30 AND salary > 50000`.
   - Click the "Add Rule" button to save the rule to the database.

3. **View Available Rules**:
   - The list of all available rules is displayed on the page.

4. **Combine Rules**:
   - Select multiple rules and choose an operator (`AND` or `OR`) to combine them.
   - The combined rule will be evaluated and displayed.

5. **Evaluate Rules**:
   - Enter user data in JSON format (e.g., `{"age": 35, "salary": 60000}`).
   - Click "Evaluate Rules" to apply the rules against the user data.

### API Endpoints

You can interact with the Rule Engine using these API endpoints:

1. **Add Rule**: Add a new rule to the database.
   ```http
   POST /add_rule
   {
     "rule": "age > 30 AND salary > 50000"
   }
   ```

2. **Combine Rules**: Combine multiple rules using logical operators.
   ```http
   POST /combine_rules
   {
     "rule_ids": [1, 2],
     "operator": "AND"
   }
   ```

3. **Evaluate Rules**: Evaluate rules against user data.
   ```http
   POST /evaluate
   {
     "rule_string": "age > 30 AND salary > 50000",
     "user_data": {"age": 35, "salary": 60000}
   }
   ```

## Rule Parsing and Evaluation

### Abstract Syntax Tree (AST)

- The rule string is parsed into tokens and then converted into an AST.
- The AST represents the logical structure of the rule, and is evaluated using recursive methods.

### Rule Parsing Example

For the rule `age > 30 AND salary > 50000`, the engine:
1. **Tokenizes** the string into components like `['age', '>', '30', 'AND', 'salary', '>', '50000']`.
2. **Parses** these tokens into an AST using the `parse_expression` function.
3. **Evaluates** the AST against the user data by recursively checking each condition.

### Node Class

The `Node` class represents operands and operators in the AST. Each node has:
- `type`: Operand or Operator.
- `value`: The actual condition or operator (e.g., `age > 30` or `AND`).
- `left` and `right`: Pointers to child nodes for operators.

## Error Handling

- **Invalid Rules**: If the rule format is invalid, a descriptive error message is returned.
- **Evaluation Errors**: If user data is missing required fields or conditions are misformatted, the evaluation will fail with an appropriate error message.

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License.

---

Feel free to adjust the content depending on your specific project needs or setup.

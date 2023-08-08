from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Sample data for the tables
table1_data = [
    {'id': 1, 'name': 'John'},
    {'id': 2, 'name': 'Alice'},
    {'id': 3, 'name': 'Bob'}
]

table2_data = [
    {'id': 1, 'role': 'Teacher'},
    {'id': 2, 'role': 'Student'},
    {'id': 3, 'role': 'Staff'}
]

@app.route('/')
def index():
    return render_template('list.html', table1_data=table1_data)

@app.route('/get_table2_data/<int:table1_id>')
def get_table2_data(table1_id):
    # Simulate fetching the data for table 2 based on the selected ID from table 1
    selected_data = table2_data[table1_id - 1]
    return jsonify(selected_data)

if __name__ == '__main__':
    app.run()

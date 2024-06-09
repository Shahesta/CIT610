from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
DATABASE = 'crud.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        db.commit()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    return items

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form['description']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
    db.commit()
    return f'item[{id}]: Added Successfully'

@app.route('/update/<int:id>', methods=['POST'])
def update_item(id):
    db = get_db()
    cursor = db.cursor()
    name = request.form['name']
    description = request.form['description']
    cursor.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (name, description, id))
    db.commit()
    return f'item[{id}]: Updated Successfully'


@app.route('/delete/<int:id>')
def delete_item(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (id,))
    db.commit()
    return f'item[{id}]: Deleted Successfully'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    print('Server Started')
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__) #creats an application named after file (app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres: @localhost:5432/todoapp'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


#db.create_all() #the tables are created for all the models that have been called


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description'] #the second value is default if empty
        todo = Todo(description2=description)
        db.session.add(todo)
        db.session.commit()
        return jsonify({
            'description': todo.description
        })
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.all())


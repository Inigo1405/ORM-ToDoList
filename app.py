from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'


db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    category = db.Column(db.String(120))
    status = db.Column(db.Boolean, nullable=False)
    created_Date = db.Column(db.TIMESTAMP, nullable=False)
    update = db.Column(db.TIMESTAMP, nullable=False)
    
    def __init__(self, name, category, status):    
        self.name = name
        self.category = category
        self.status = status
        self.created_Date = datetime.now()
        
    def __repr__(self):
        return f'<Task {self.name}>'
    
    
    
BASE_URL = '/api/v1'
    
@app.route('/')
def index():
    return "Welcome to my ORM app toDoList!"


@app.route(BASE_URL + '/new')
def create():
    task = Task(name='First Task', status=False, category='study')
    db.session.add(task)
    db.session.commit()
    return 'Task added'


@app.route(BASE_URL + '/read')
def read():
    tasks = Task.query.all()
    print(tasks)
    return 'Task fetched'
    
    
# @app.route(BASE_URL + '/update')
# def update():
#     return


# @app.route(BASE_URL + '/delete')
# def delete():
#     return



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Tables created...")
    app.run(debug=False)
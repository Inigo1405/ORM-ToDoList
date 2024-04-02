from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
BASE_URL = '/api/v1'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    category = db.Column(db.String(120))
    status = db.Column(db.Boolean, nullable=False)
    created_Date = db.Column(db.TIMESTAMP, nullable=False)
    update = db.Column(db.TIMESTAMP, nullable=False)
    
    def __init__(self, name, status, category=None):    
        self.name = name
        self.category = category
        self.status = status
        self.created_Date = datetime.now()
        self.update = datetime.now()
        
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_Date": self.created_Date,
            "status": self.status,
            "update": self.update
        }
        
    def __repr__(self):
        return f'<Task {self.name}>'
    


@app.route(BASE_URL + '/new', methods=['POST'])
def create():
    if not request.json or 'name' not in request.json:
        abort(400)
        
    task = Task(name=request.json['name'], status=False)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_json()), 201


@app.route(BASE_URL + '/read', methods=['GET'])
def read():
    tasks = Task.query.all()
    return jsonify([task.to_json() for task in tasks])
    
    
@app.route(BASE_URL + '/update/<id>', methods=['PUT'])
def update(id:int):
    task = Task.query.get(id)
    
    if not task:
        abort(400)
        
    task.status = not task.status
    db.session.commit()
    return jsonify(task.to_json()), 201


@app.route(BASE_URL + '/delete', methods=['DELETE'])
def delete(id):
    task = Task.query.get(id)
    if not task:
        abort(400)
        
    db.session.delete(task)
    db.session.commit()
    
    return jsonify(task.to_json())


# --- MAIN -------------------------------------------------------------------- 
@app.route('/')
def index():
    return "Welcome to my ORM app toDoList!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Tables created...")
    app.run(debug=False)
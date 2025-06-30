from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)
CORS(app)

# Database Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7), default='#007bff')  # Hex color code
    tasks = db.relationship('Task', backref='category_ref', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'task_count': len(self.tasks)
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default='medium')  # high, medium, low
    due_date = db.Column(db.Date, nullable=True)
    reminder_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'reminder_time': self.reminder_time.isoformat() if self.reminder_time else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'category_id': self.category_id,
            'category': self.category_ref.name if self.category_ref else None
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Category endpoints
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Category name is required'}), 400
    
    category = Category(
        name=data['name'],
        color=data.get('color', '#007bff')
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        return jsonify(category.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Category name must be unique'}), 400

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return '', 204

# Task endpoints
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Query parameters for filtering
    category_id = request.args.get('category_id', type=int)
    priority = request.args.get('priority')
    completed = request.args.get('completed')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'created_at')
    
    query = Task.query
    
    # Apply filters
    if category_id:
        query = query.filter(Task.category_id == category_id)
    
    if priority:
        query = query.filter(Task.priority == priority)
    
    if completed is not None:
        completed_bool = completed.lower() == 'true'
        query = query.filter(Task.completed == completed_bool)
    
    if search:
        query = query.filter(
            db.or_(
                Task.title.contains(search),
                Task.description.contains(search)
            )
        )
    
    # Apply sorting
    if sort_by == 'priority':
        # Custom priority order: high, medium, low
        priority_order = db.case(
            (Task.priority == 'high', 1),
            (Task.priority == 'medium', 2),
            (Task.priority == 'low', 3),
            else_=4
        )
        query = query.order_by(priority_order, Task.created_at.desc())
    elif sort_by == 'due_date':
        query = query.order_by(Task.due_date.asc().nullslast(), Task.created_at.desc())
    else:
        query = query.order_by(Task.created_at.desc())
    
    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Task title is required'}), 400
    
    # Parse due date
    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid due date format. Use YYYY-MM-DD'}), 400
    
    # Parse reminder time
    reminder_time = None
    if data.get('reminder_time'):
        try:
            reminder_time = datetime.fromisoformat(data['reminder_time'])
        except ValueError:
            return jsonify({'error': 'Invalid reminder time format'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        due_date=due_date,
        reminder_time=reminder_time,
        category_id=data.get('category_id')
    )
    
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    if 'priority' in data:
        task.priority = data['priority']
    if 'category_id' in data:
        task.category_id = data['category_id']
    
    # Update due date
    if 'due_date' in data:
        if data['due_date']:
            try:
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid due date format. Use YYYY-MM-DD'}), 400
        else:
            task.due_date = None
    
    # Update reminder time
    if 'reminder_time' in data:
        if data['reminder_time']:
            try:
                task.reminder_time = datetime.fromisoformat(data['reminder_time'])
            except ValueError:
                return jsonify({'error': 'Invalid reminder time format'}), 400
        else:
            task.reminder_time = None
    
    task.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(task.to_dict())

# Dashboard/stats endpoint
@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter(Task.completed == True).count()
    pending_tasks = total_tasks - completed_tasks
    overdue_tasks = Task.query.filter(
        Task.due_date < date.today(),
        Task.completed == False
    ).count()
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks
    })

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default categories if none exist
        if Category.query.count() == 0:
            default_categories = [
                Category(name='Personal', color='#28a745'),
                Category(name='Work', color='#007bff'),
                Category(name='Urgent', color='#dc3545'),
                Category(name='Shopping', color='#ffc107')
            ]
            for category in default_categories:
                db.session.add(category)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

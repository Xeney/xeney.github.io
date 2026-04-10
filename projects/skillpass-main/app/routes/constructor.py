from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import Path, Stage, Step, Test, Question, Answer
from app.decorators import admin_required
from app import db  # Это должно работать, но давай импортируем по-другому
import json

bp = Blueprint('constructor', __name__, url_prefix='/constructor')

@bp.route('/')
@login_required
@admin_required
def index():
    """Главная страница конструктора"""
    paths = Path.query.all()
    return render_template('constructor/index.html', paths=paths)

@bp.route('/path/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_path():
    """Создание нового пути"""
    if request.method == 'POST':
        path = Path(
            title=request.form['title'],
            description=request.form['description'],
            difficulty=request.form['difficulty']
        )
        db.session.add(path)
        db.session.commit()
        flash('Путь успешно создан!', 'success')
        return redirect(url_for('constructor.edit_path', path_id=path.id))
    
    return render_template('constructor/path_form.html')

@bp.route('/path/<int:path_id>/edit')
@login_required
@admin_required
def edit_path(path_id):
    """Редактирование пути"""
    path = Path.query.get_or_404(path_id)
    return render_template('constructor/path_editor.html', path=path)

@bp.route('/api/path/<int:path_id>')
@login_required
@admin_required
def get_path_data(path_id):
    """API для получения данных пути"""
    path = Path.query.get_or_404(path_id)
    data = {
        'id': path.id,
        'title': path.title,
        'description': path.description,
        'difficulty': path.difficulty,
        'stages': []
    }
    
    for stage in path.stages:
        stage_data = {
            'id': stage.id,
            'title': stage.title,
            'description': stage.description,
            'order_index': stage.order_index,
            'steps': []
        }
        
        for step in stage.steps:
            step_data = {
                'id': step.id,
                'title': step.title,
                'type': step.type,
                'content': step.content,
                'xp_reward': step.xp_reward,
                'order_index': step.order_index
            }
            
            if step.type == 'test' and step.test:
                step_data['test'] = {
                    'id': step.test.id,
                    'passing_score': step.test.passing_score,
                    'questions': []
                }
                
                for question in step.test.questions:
                    question_data = {
                        'id': question.id,
                        'text': question.text,
                        'order_index': question.order_index,
                        'answers': []
                    }
                    
                    for answer in question.answers:
                        question_data['answers'].append({
                            'id': answer.id,
                            'text': answer.text,
                            'is_correct': answer.is_correct
                        })
                    
                    step_data['test']['questions'].append(question_data)
            
            stage_data['steps'].append(step_data)
        
        data['stages'].append(stage_data)
    
    return jsonify(data)

@bp.route('/api/stage/new', methods=['POST'])
@login_required
@admin_required
def new_stage():
    """API для создания этапа"""
    data = request.json
    stage = Stage(
        path_id=data['path_id'],
        title=data['title'],
        description=data.get('description', ''),
        order_index=data['order_index']
    )
    db.session.add(stage)
    db.session.commit()
    return jsonify({'id': stage.id, 'title': stage.title})

@bp.route('/api/step/new', methods=['POST'])
@login_required
@admin_required
def new_step():
    """API для создания шага"""
    data = request.json
    step = Step(
        stage_id=data['stage_id'],
        title=data['title'],
        type=data['type'],
        content=data.get('content', ''),
        xp_reward=data.get('xp_reward', 10),
        order_index=data['order_index']
    )
    db.session.add(step)
    db.session.flush()
    
    if data['type'] == 'test':
        test = Test(
            step_id=step.id,
            passing_score=data.get('passing_score', 80)
        )
        db.session.add(test)
    
    db.session.commit()
    return jsonify({'id': step.id, 'title': step.title})

@bp.route('/api/question/new', methods=['POST'])
@login_required
@admin_required
def new_question():
    """API для создания вопроса"""
    data = request.json
    question = Question(
        test_id=data['test_id'],
        text=data['text'],
        order_index=data['order_index']
    )
    db.session.add(question)
    db.session.flush()
    
    for answer_data in data['answers']:
        answer = Answer(
            question_id=question.id,
            text=answer_data['text'],
            is_correct=answer_data['is_correct']
        )
        db.session.add(answer)
    
    db.session.commit()
    return jsonify({'id': question.id})

@bp.route('/api/update', methods=['POST'])
@login_required
@admin_required
def update_item():
    """API для обновления элементов"""
    data = request.json
    item_type = data['type']
    item_id = data['id']
    
    if item_type == 'stage':
        item = Stage.query.get(item_id)
        item.title = data['title']
        item.description = data.get('description', '')
    elif item_type == 'step':
        item = Step.query.get(item_id)
        item.title = data['title']
        item.content = data.get('content', '')
        item.xp_reward = data.get('xp_reward', 10)
    elif item_type == 'question':
        item = Question.query.get(item_id)
        item.text = data['text']
    
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/api/delete', methods=['POST'])
@login_required
@admin_required
def delete_item():
    """API для удаления элементов"""
    data = request.json
    item_type = data['type']
    item_id = data['id']
    
    if item_type == 'stage':
        item = Stage.query.get(item_id)
    elif item_type == 'step':
        item = Step.query.get(item_id)
    elif item_type == 'question':
        item = Question.query.get(item_id)
    elif item_type == 'answer':
        item = Answer.query.get(item_id)
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/api/reorder', methods=['POST'])
@login_required
@admin_required
def reorder_items():
    """API для изменения порядка"""
    data = request.json
    items = data['items']
    
    for item_data in items:
        if item_data['type'] == 'stage':
            item = Stage.query.get(item_data['id'])
            item.order_index = item_data['order']
        elif item_data['type'] == 'step':
            item = Step.query.get(item_data['id'])
            item.order_index = item_data['order']
    
    db.session.commit()
    return jsonify({'success': True})
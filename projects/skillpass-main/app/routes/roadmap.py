from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, session
from flask_login import login_required, current_user
from app import db
from app.models import Path, Stage, Step, Test, Question, Answer, UserProgress, XPLog, SavedPath, UserAnswer
from datetime import datetime, timezone
import math

bp = Blueprint('roadmap', __name__, url_prefix='/roadmap')

def check_step_available(step, user_id):
    """Проверяет, доступен ли шаг для прохождения"""
    # Если это первый шаг в этапе - доступен
    stage_steps = Step.query.filter_by(stage_id=step.stage_id).order_by(Step.order_index).all()
    
    # Находим индекс текущего шага
    current_index = -1
    for i, s in enumerate(stage_steps):
        if s.id == step.id:
            current_index = i
            break
    
    # Если это первый шаг - доступен
    if current_index <= 0:
        return True, None
    
    # Проверяем, пройден ли предыдущий шаг
    previous_step = stage_steps[current_index - 1]
    previous_progress = UserProgress.query.filter_by(
        user_id=user_id,
        step_id=previous_step.id,
        completed=True
    ).first()
    
    if not previous_progress:
        return False, previous_step
    
    return True, None

@bp.route('/')
def catalog():
    """Каталог путей - доступен всем"""
    paths = Path.query.all()
    
    completed_steps = []
    completed_count = 0
    in_progress_count = 0
    
    if current_user.is_authenticated:
        completed_steps = [p.step_id for p in UserProgress.query.filter_by(
            user_id=current_user.id, completed=True).all()]
        
        # Считаем пройденные и начатые пути
        for path in paths:
            total_steps = 0
            completed_in_path = 0
            for stage in path.stages:
                total_steps += len(stage.steps)
                for step in stage.steps:
                    if step.id in completed_steps:
                        completed_in_path += 1
            
            if completed_in_path == total_steps and total_steps > 0:
                completed_count += 1
            elif completed_in_path > 0:
                in_progress_count += 1
    
    return render_template('roadmap/catalog.html', 
                          paths=paths,
                          completed_steps=completed_steps,
                          completed_count=completed_count,
                          in_progress_count=in_progress_count)

@bp.route('/<int:path_id>')
def view(path_id):
    path = Path.query.get_or_404(path_id)
    stages = Stage.query.filter_by(path_id=path_id).order_by(Stage.order_index).all()
    
    completed_steps = []
    saved_paths = []
    available_steps = []  # Список доступных шагов
    total_steps = 0
    completed_count = 0
    theory_count = 0
    theory_total = 0
    test_count = 0
    test_total = 0
    earned_xp = 0
    
    # Считаем общее количество XP в пути
    total_xp = 0
    for stage in stages:
        for step in stage.steps:
            total_xp += step.xp_reward
            total_steps += 1
            if step.type == 'theory':
                theory_total += 1
            else:
                test_total += 1
    
    if current_user.is_authenticated:
        completed_steps = [p.step_id for p in UserProgress.query.filter_by(
            user_id=current_user.id, completed=True).all()]
        saved_paths = [s.path_id for s in SavedPath.query.filter_by(user_id=current_user.id).all()]
        
        # Определяем доступные шаги
        for stage in stages:
            stage_steps = sorted(stage.steps, key=lambda x: x.order_index)
            for i, step in enumerate(stage_steps):
                # Шаг доступен если:
                # 1. Он уже пройден
                # 2. Это первый шаг в этапе
                # 3. Предыдущий шаг пройден
                if step.id in completed_steps:
                    available_steps.append(step.id)
                    completed_count += 1
                    earned_xp += step.xp_reward
                    if step.type == 'theory':
                        theory_count += 1
                    else:
                        test_count += 1
                elif i == 0:  # Первый шаг в этапе всегда доступен
                    available_steps.append(step.id)
                else:
                    # Проверяем, пройден ли предыдущий шаг
                    prev_step = stage_steps[i-1]
                    if prev_step.id in completed_steps:
                        available_steps.append(step.id)
    
    progress_percent = int((completed_count / total_steps * 100)) if total_steps > 0 else 0
    
    return render_template('roadmap/view.html', 
                          path=path, 
                          stages=stages, 
                          completed_steps=completed_steps, 
                          saved_paths=saved_paths,
                          available_steps=available_steps,  # Важно!
                          total_steps=total_steps,
                          completed_count=completed_count,
                          progress_percent=progress_percent,
                          theory_count=theory_count,
                          theory_total=theory_total,
                          test_count=test_count,
                          test_total=test_total,
                          earned_xp=earned_xp,
                          total_xp=total_xp)

@bp.route('/step/<int:step_id>')
@login_required  # Только для авторизованных!
def view_step(step_id):
    """Просмотр шага (теории или теста) - только для авторизованных"""
    step = Step.query.get_or_404(step_id)
    
    # Проверяем авторизацию
    is_completed = False
    completed_steps = []
    step_available = True
    required_step = None
    
    if current_user.is_authenticated:
        # Проверяем, пройден ли шаг
        progress = UserProgress.query.filter_by(
            user_id=current_user.id, 
            step_id=step_id,
            completed=True
        ).first()
        is_completed = progress is not None
        
        # Получаем все пройденные шаги
        completed_steps = [p.step_id for p in UserProgress.query.filter_by(
            user_id=current_user.id, completed=True).all()]
        
        # Проверяем доступность шага
        if not is_completed:
            step_available, required_step = check_step_available(step, current_user.id)
    
    if step.type == 'theory':
        return render_template('roadmap/step.html', 
                             step=step, 
                             is_completed=is_completed,
                             completed_steps=completed_steps,
                             step_available=step_available,
                             required_step=required_step)
    else:  # test
        # Проверяем, можно ли проходить тест
        if not is_completed and not step_available:
            flash(f'Сначала нужно пройти шаг: {required_step.title}', 'warning')
            return redirect(url_for('roadmap.view_step', step_id=required_step.id))
        
        session['current_test'] = step_id
        return render_template('roadmap/test.html', 
                             step=step,
                             completed_steps=completed_steps,
                             is_completed=is_completed)

@bp.route('/step/<int:step_id>/complete', methods=['POST'])
@login_required
def complete_step(step_id):
    """Отметить шаг как пройденный (для теории)"""
    step = Step.query.get_or_404(step_id)
    
    if step.type != 'theory':
        flash('Этот шаг нельзя отметить как пройденный таким способом', 'warning')
        return redirect(url_for('roadmap.view_step', step_id=step_id))
    
    # Проверяем доступность шага
    step_available, required_step = check_step_available(step, current_user.id)
    if not step_available:
        flash(f'Сначала нужно пройти шаг: {required_step.title}', 'warning')
        return redirect(url_for('roadmap.view_step', step_id=required_step.id))
    
    # Проверяем, не пройден ли уже шаг
    existing_progress = UserProgress.query.filter_by(
        user_id=current_user.id, 
        step_id=step_id, 
        completed=True
    ).first()
    
    if existing_progress:
        flash('Вы уже прошли этот шаг', 'info')
        return redirect(url_for('roadmap.view_step', step_id=step_id))
    
    # Начисляем XP
    xp_amount = step.xp_reward
    profile = current_user.profile
    profile.xp += xp_amount
    
    # Логируем
    xp_log = XPLog(
        user_id=current_user.id, 
        amount=xp_amount, 
        reason=f'Пройден шаг: {step.title}'
    )
    db.session.add(xp_log)
    
    # Отмечаем шаг как пройденный
    progress = UserProgress(
        user_id=current_user.id, 
        step_id=step_id,
        completed=True,
        completed_at=datetime.now(timezone.utc)
    )
    db.session.add(progress)
    
    db.session.commit()
    
    flash(f'🎉 Шаг пройден! Вы получили {xp_amount} XP', 'success')
    return redirect(url_for('roadmap.view_step', step_id=step_id))

@bp.route('/step/<int:step_id>/submit', methods=['POST'])
@login_required
def submit_test(step_id):
    # Проверяем, что тест был начат
    if session.get('current_test') != step_id:
        flash('Ошибка при отправке теста', 'danger')
        return redirect(url_for('roadmap.view_step', step_id=step_id))
    
    step = Step.query.get_or_404(step_id)
    test = step.test
    
    if not test:
        abort(404)
    
    # Проверяем доступность шага
    step_available, required_step = check_step_available(step, current_user.id)
    if not step_available:
        flash(f'Сначала нужно пройти шаг: {required_step.title}', 'warning')
        return redirect(url_for('roadmap.view_step', step_id=required_step.id))
    
    # Проверяем, не проходил ли уже пользователь этот тест
    existing_progress = UserProgress.query.filter_by(
        user_id=current_user.id, 
        step_id=step_id, 
        completed=True
    ).first()
    
    if existing_progress:
        flash('Вы уже проходили этот тест', 'warning')
        return redirect(url_for('roadmap.view_step', step_id=step_id))
    
    # Собираем ответы
    correct_count = 0
    total_questions = len(test.questions)
    answers_data = []
    
    # Очищаем старые ответы на этот тест (если были)
    UserAnswer.query.filter_by(
        user_id=current_user.id,
        test_id=test.id
    ).delete()
    
    for question in test.questions:
        answer_key = f'question_{question.id}'
        selected_answer_id = request.form.get(answer_key, type=int)
        
        if selected_answer_id:
            answer = Answer.query.get(selected_answer_id)
            is_correct = answer and answer.is_correct
            
            # Сохраняем ответ пользователя
            user_answer = UserAnswer(
                user_id=current_user.id,
                test_id=test.id,
                question_id=question.id,
                answer_id=selected_answer_id,
                is_correct=is_correct
            )
            db.session.add(user_answer)
            
            if is_correct:
                correct_count += 1
            
            answers_data.append({
                'question': question.text,
                'answer': answer.text if answer else 'Не выбран',
                'is_correct': is_correct
            })
        else:
            answers_data.append({
                'question': question.text,
                'answer': 'Не выбран',
                'is_correct': False
            })
    
    if total_questions == 0:
        score = 100
    else:
        score = (correct_count / total_questions) * 100
    
    # Сохраняем результаты в сессии
    session['last_test_results'] = {
        'score': score,
        'passing_score': test.passing_score,
        'correct': correct_count,
        'total': total_questions,
        'answers': answers_data,
        'step_title': step.title,
        'xp_reward': step.xp_reward
    }
    
    # Проверяем, пройден ли тест
    if score >= test.passing_score:
        # Начисляем XP
        xp_amount = step.xp_reward
        profile = current_user.profile
        profile.xp += xp_amount
        
        # Логируем
        xp_log = XPLog(
            user_id=current_user.id, 
            amount=xp_amount, 
            reason=f'Тест пройден: {step.title}'
        )
        db.session.add(xp_log)
        
        # Отмечаем шаг как пройденный
        progress = UserProgress(
            user_id=current_user.id, 
            step_id=step_id,
            completed=True,
            completed_at=datetime.now(timezone.utc)
        )
        db.session.add(progress)
        
        db.session.commit()
        
        # Очищаем сессию
        session.pop('current_test', None)
        
        flash(f'🎉 Поздравляем! Тест пройден! Вы набрали {score:.1f}% и получили {xp_amount} XP', 'success')
    else:
        # При неудаче сохраняем ответы, но не отмечаем шаг
        db.session.commit()
        flash(f'❌ Тест не пройден. Вы набрали {score:.1f}% при проходном {test.passing_score}%. Попробуйте ещё раз!', 'danger')
    
    return redirect(url_for('roadmap.test_results', step_id=step_id))

@bp.route('/step/<int:step_id>/results')
@login_required
def test_results(step_id):
    step = Step.query.get_or_404(step_id)
    results = session.get('last_test_results')
    
    if not results:
        flash('Нет результатов для отображения', 'warning')
        return redirect(url_for('roadmap.view_step', step_id=step_id))
    
    return render_template('roadmap/test_results.html', step=step, results=results)

@bp.route('/save-path/<int:path_id>', methods=['POST'])
@login_required
def save_path(path_id):
    path = Path.query.get_or_404(path_id)
    
    saved = SavedPath.query.filter_by(
        user_id=current_user.id, 
        path_id=path_id
    ).first()
    
    if saved:
        db.session.delete(saved)
        db.session.commit()
        flash(f'Путь "{path.title}" удалён из избранного', 'info')
    else:
        saved_path = SavedPath(user_id=current_user.id, path_id=path_id)
        db.session.add(saved_path)
        db.session.commit()
        flash(f'Путь "{path.title}" добавлен в избранное', 'success')
    
    return redirect(url_for('roadmap.view', path_id=path_id))

@bp.route('/saved-paths')
@login_required
def saved_paths():
    saved_paths = SavedPath.query.filter_by(user_id=current_user.id).order_by(SavedPath.saved_at.desc()).all()
    return render_template('roadmap/saved_paths.html', saved_paths=saved_paths)

@bp.route('/retry-test/<int:step_id>', methods=['POST'])
@login_required
def retry_test(step_id):
    """Очищает старые ответы и позволяет перепройти тест"""
    step = Step.query.get_or_404(step_id)
    
    if step.type != 'test':
        flash('Это не тест', 'warning')
        return redirect(url_for('roadmap.view_step', step_id=step_id))
    
    # Проверяем, был ли тест пройден
    progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        step_id=step_id,
        completed=True
    ).first()
    
    if progress:
        flash('Вы уже успешно прошли этот тест', 'info')
        return redirect(url_for('roadmap.view_step', step_id=step_id))
    
    # Очищаем старые ответы
    UserAnswer.query.filter_by(
        user_id=current_user.id,
        test_id=step.test.id
    ).delete()
    db.session.commit()
    
    # Устанавливаем новую сессию
    session['current_test'] = step_id
    flash('Попробуйте ещё раз!', 'info')
    return redirect(url_for('roadmap.view_step', step_id=step_id))
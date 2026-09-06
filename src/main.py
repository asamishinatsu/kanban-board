from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Board, CardList, Card
from datetime import datetime
from secret import SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'board_list'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
@app.route('/board_list')
def board_list():
    if current_user.is_authenticated:
        boards = Board.query.filter_by(user_id=current_user.user_id) \
            .order_by(Board.board_id.desc()).all()
    else:
        boards = []
    return render_template('board_list.html', boards=boards)


@app.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')

    user = User.query.filter_by(user_name=user_name).first()

    if user is None or not user.check_password(password):
        return {'success': False, 'error': 'Invalid username or password'}, 400

    login_user(user)
    return {'success': True}


@app.route('/register', methods=['POST'])
def register():
    user_name = request.form.get('user_name')
    password = request.form.get('password')

    existing_user = User.query.filter_by(user_name=user_name).first()
    if existing_user:
        return {'success': False, 'error': 'User with that name already exists'}, 400

    new_user = User(user_name=user_name)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return {'success': True}


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('board_list'))


@app.route('/board/<int:board_id>')
@login_required
def board_detail(board_id):
    board = Board.query.get_or_404(board_id)

    if board.user_id != current_user.user_id:
        abort(403)

    return render_template('board.html', board=board)


@app.route('/board/create', methods=['POST'])
@login_required
def create_board():
    board_name = request.form.get('board_name')
    board_description = request.form.get('board_description')

    if not board_name:
        flash('Enter a board name')
        return redirect(url_for('board_list'))

    new_board = Board(
        board_name=board_name,
        board_description=board_description,
        user_id=current_user.user_id
    )

    db.session.add(new_board)
    db.session.commit()

    return redirect(url_for('board_list'))


@app.route('/board/<int:board_id>/list/create', methods=['POST'])
@login_required
def create_list(board_id):
    board = Board.query.get_or_404(board_id)

    if board.user_id != current_user.user_id:
        abort(403)

    list_name = request.form.get('list_name')

    if not list_name:
        flash('Enter a list name')
        return redirect(url_for('board_detail', board_id=board_id))

    # позиция — следующая по порядку среди уже существующих списков доски
    max_position = db.session.query(db.func.max(CardList.list_position)) \
        .filter_by(board_id=board_id).scalar()
    next_position = (max_position or 0) + 1

    new_list = CardList(
        list_name=list_name,
        list_position=next_position,
        board_id=board_id
    )

    db.session.add(new_list)
    db.session.commit()

    return redirect(url_for('board_detail', board_id=board_id))


@app.route('/list/<int:list_id>/card/create', methods=['POST'])
@login_required
def create_card(list_id):
    board_list = CardList.query.get_or_404(list_id)

    if board_list.board.user_id != current_user.user_id:
        abort(403)

    card_title = request.form.get('card_title')
    importance = request.form.get('importance')

    if not card_title:
        flash('Enter a card title')
        return redirect(url_for('board_detail', board_id=board_list.board_id))

    if importance not in ('low', 'medium', 'high'):
        flash('Invalid priority')
        return redirect(url_for('board_detail', board_id=board_list.board_id))

    max_position = db.session.query(db.func.max(Card.card_position)) \
        .filter_by(list_id=list_id).scalar()
    next_position = (max_position or 0) + 1

    due_date_str = request.form.get('due_date')
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

    new_card = Card(
        card_title=card_title,
        importance=importance,
        due_date=due_date,
        card_position=next_position,
        list_id=list_id
    )

    db.session.add(new_card)
    db.session.commit()

    return redirect(url_for('board_detail', board_id=board_list.board_id))


@app.route('/board/<int:board_id>/edit', methods=['POST'])
@login_required
def edit_board(board_id):
    board = Board.query.get_or_404(board_id)

    if board.user_id != current_user.user_id:
        abort(403)

    board_name = request.form.get('board_name')
    board_description = request.form.get('board_description')

    if not board_name:
        flash('Enter a board name')
        return redirect(url_for('board_list'))

    board.board_name = board_name
    board.board_description = board_description

    db.session.commit()

    return redirect(url_for('board_list'))


@app.route('/list/<int:list_id>/edit', methods=['POST'])
@login_required
def edit_list(list_id):
    board_list = CardList.query.get_or_404(list_id)

    if board_list.board.user_id != current_user.user_id:
        abort(403)

    list_name = request.form.get('list_name')

    if not list_name:
        flash('Enter a list name')
        return redirect(url_for('board_detail', board_id=board_list.board_id))

    board_list.list_name = list_name

    db.session.commit()

    return redirect(url_for('board_detail', board_id=board_list.board_id))


@app.route('/card/<int:card_id>/edit', methods=['POST'])
@login_required
def edit_card(card_id):
    card = Card.query.get_or_404(card_id)

    if card.list.board.user_id != current_user.user_id:
        abort(403)

    card_title = request.form.get('card_title')
    importance = request.form.get('importance')

    if not card_title:
        flash('Enter a card title')
        return redirect(url_for('board_detail', board_id=card.list.board_id))

    if importance not in ('low', 'medium', 'high'):
        flash('Invalid priority')
        return redirect(url_for('board_detail', board_id=card.list.board_id))

    due_date_str = request.form.get('due_date')
    card.due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

    card.card_title = card_title
    card.importance = importance

    db.session.commit()

    return redirect(url_for('board_detail', board_id=card.list.board_id))


@app.route('/board/<int:board_id>/delete', methods=['POST'])
@login_required
def delete_board(board_id):
    board = Board.query.get_or_404(board_id)

    if board.user_id != current_user.user_id:
        abort(403)

    db.session.delete(board)
    db.session.commit()

    return redirect(url_for('board_list'))


@app.route('/list/<int:list_id>/delete', methods=['POST'])
@login_required
def delete_list(list_id):
    board_list = CardList.query.get_or_404(list_id)

    if board_list.board.user_id != current_user.user_id:
        abort(403)

    board_id = board_list.board_id

    db.session.delete(board_list)
    db.session.commit()

    return redirect(url_for('board_detail', board_id=board_id))


@app.route('/card/<int:card_id>/delete', methods=['POST'])
@login_required
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)

    if card.list.board.user_id != current_user.user_id:
        abort(403)

    board_id = card.list.board_id

    db.session.delete(card)
    db.session.commit()

    return redirect(url_for('board_detail', board_id=board_id))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
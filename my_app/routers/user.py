from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from backend.db import db
from flask_login import LoginManager, logout_user, login_required, login_user, current_user

from routers.forms import LoginForm, RegistrationForm

user_bp = Blueprint('user_bp', __name__, template_folder="templates")
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@user_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        data = {
            'username': form.username.data,
            'first_name': form.first_name.data,
            'email': form.email.data,
            'password': form.password.data
        }

        existing_user = User.query.filter((User.email == data['email']) | (User.username == data['username'])).first()
        if existing_user:
            flash("Пользователь с таким email или username уже существует!")
            return redirect(url_for('.show_register'))

        new_user = User(
            username=data['username'],
            first_name=data['first_name'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Пользователь успешно зарегистрирован! Пожалуйста, войдите.")
        return redirect(url_for('.show_login'))

    return render_template('users/registration_page.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {
            'email': form.email.data,
            'password': form.password.data
        }
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            login_user(user)
            flash("Вы вошли в систему!", "success")
            next_url = request.args.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(url_for('main.home'))
        else:
            flash("Неверный email или пароль!", "danger")
            return redirect(url_for('.show_login'))
    return render_template('users/login.html', form=form)


@user_bp.route('/logout', methods=['GET'])
def user_logout():
    logout_user()
    flash("Вы вышли из системы!", "info")
    return redirect(url_for('main.home'))


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "email": user.email
        }), 200
    return jsonify({"message": "Пользователь не найден"}), 404


@user_bp.route('/register', methods=['GET'])
def show_register():
    return render_template('users/registration_page.html')


@user_bp.route('/login', methods=['GET'])
def show_login():
    return render_template('users/login.html')

from flask import render_template, request, redirect, flash, url_for
from .dao import load_books, load_book, auth_user
from flask_login import login_user, logout_user, login_required


def index():
    return render_template('pages/index.html', 
                        lastest=load_books(latest=True)
                    )


def collections():
    return render_template('pages/collections.html')


def detail(id):
    return render_template('pages/detail.html', book=load_book(book_id=id))


def about():
    return render_template('pages/about.html')


def login_admin():
    email = request.form.get('email')
    password = request.form.get('password')
    user = auth_user(email=email, password=password)

    if user and user.is_admin():
        flash(f"Welcome to {user.username} comeback!", category="success")
        login_user(user=user)
        return redirect(url_for('admin.index'))

    flash("Invalid email or password. Please try again.", category="warning")
    return redirect(url_for('admin.index'))


def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        user = auth_user(email=email, password=password)
        
        if user:
            flash(f"Welcome to {user.username} comeback!", category="success")
            login_user(user=user, remember=remember)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('pages/login.html')


def register():
    pass


def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
def profile():
    return render_template('pages/profile.html')
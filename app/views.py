from flask import render_template, request, session, redirect, url_for


def index():
    return render_template('pages/index.html')


def login():
    if request.method == 'POST':
        pass


def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
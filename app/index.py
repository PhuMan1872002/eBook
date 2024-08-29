from app import app, views, login_manager, dao
from flask import render_template


@login_manager.user_loader
def user_loader(user_id):
    return dao.load_users(user_id)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('pages/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('pages/500.html'), 500


app.add_url_rule('/', view_func=views.index,  methods=['GET'])
app.add_url_rule('/login', view_func=views.login, methods=['GET', 'POST'])
from flask import session, render_template, request
from app import app, login_manager, controllers, dao, utils
from datetime import datetime, timezone
from flask_login import current_user

app.add_url_rule('/', view_func=controllers.index)
app.add_url_rule('/collections', view_func=controllers.collections)
app.add_url_rule('/collections/<int:id>/', view_func=controllers.detail)
app.add_url_rule('/about', view_func=controllers.about)
app.add_url_rule('/admin/login', view_func=controllers.login_admin, methods=['post'])
app.add_url_rule('/login', view_func=controllers.login, methods=['get', 'post'])
app.add_url_rule('/logout', view_func=controllers.logout)
app.add_url_rule('/profile', view_func=controllers.profile)
app.add_url_rule('/register', view_func=controllers.register, methods=['get', 'post'])
app.add_url_rule('/change-password', view_func=controllers.change_password, methods=['post'])
app.add_url_rule('/forgot-password', view_func=controllers.forgot_password, methods=['post'])
app.add_url_rule('/reset-password', view_func=controllers.reset_password, methods=['get', 'post'])
app.add_url_rule('/api/comments/', view_func=controllers.comment, methods=['post', 'delete'])
app.add_url_rule('/api/cart/', view_func=controllers.cart, methods=['post'])
app.add_url_rule('/api/cart/<book_id>', view_func=controllers.delete_cart, methods=['delete'])
app.add_url_rule('/api/pay', view_func=controllers.pay_checkout)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        current_user.save()


@login_manager.user_loader
def user_loader(user_id):
    return dao.load_user(user_id=user_id)


@app.context_processor
def common_responses():
    return dict(categories=dao.load_categories(),
                format_price=utils.format_price,
                books=dao.load_books(
                    page=request.args.get('page', 1, type=int),
                    category=request.args.get('category', type=int),
                    keyword=request.args.get('keyword')
                ),
                cart=utils.cart_stats(session.get('cart'))
            )


@app.errorhandler(404)
def page_not_found(error):
    return render_template('pages/404.html'), 404
from app.models import User, Category


def load_user(user_id):
    return User.get(user_id)


def load_categories():
    return Category.query.filter(Category.active.__eq__(True)).all()

from sqlalchemy import extract, func
from app.models import User, Category, Book, db
from .config import Config

def load_user(user_id):
    return User.query.get(user_id)


def load_categories():
    return Category.query.filter(Category.active.__eq__(True)).all()


def load_books(
    page=1,
    per_page=Config.PAGE_SIZE,
    latest=False,
    **kwargs
):
    queries = Book.query.filter(Book.active.__eq__(True))

    category = kwargs.get('category')
    keyword = kwargs.get('keyword')
    from_price = kwargs.get('from_price')
    to_price = kwargs.get('to_price')
    release_month = kwargs.get('release_month')
    release_month_after = kwargs.get('release_month_after')
    release_month_before = kwargs.get('release_month_before')
    
    if category:
        queries = queries.filter(Book.category_id.__eq__(category))

    if keyword:
        queries = queries.filter(Book.title.contains(keyword))

    if from_price:
        queries = queries.filter(Book.price.__ge__(from_price))

    if to_price:
        queries = queries.filter(Book.price.__le__(to_price))

    if release_month:
        queries = queries.filter(
            extract('month', Book.date_created).__eq__(release_month))

    if release_month_after:
        queries = queries.filter(
            extract('month', Book.date_created).__gt__(release_month_after))

    if release_month_before:
        queries = queries.filter(
            extract('month', Book.date_created).__lt__(release_month_before))

    if latest:
        queries = queries.order_by(Book.date_created.desc())
        return queries.limit(4).all()
        
    return queries.paginate(page=page, per_page=per_page)
    
    
def load_book(book_id):
    return Book.query.get(int(book_id))


def create_user(username, email, password, **kwargs):
    user = User(
        username=username,
        email=email,
        **kwargs
    )
    user.set_password(password=password)
    user.save()
    return user


def auth_user(email, password):
    user = User.query.filter(User.email.__eq__(email)).first()
    return user if user and user.check_password(password=password) else None


def stats_books():
    return db.session.query(Category.id, Category.name, func.count(Book.id))\
        .join(Book, Book.category_id.__eq__(Category.id), isouter=True)\
        .group_by(Category.id).all()
        

def count_books():
    return Book.query.count()
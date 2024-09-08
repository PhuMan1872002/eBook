import enum
from .utils import hash_avatar_url
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Enum, DateTime, Text
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class RoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class BaseModel(db.Model):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
    date_created = Column(DateTime, default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(BaseModel, UserMixin):
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(Text)
    avatar = Column(Text, default=None)
    address = Column(String(125), nullable=True)
    phone = Column(String(10), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    last_seen = Column(DateTime)
    reset_code = Column(String(7), nullable=True, unique=True)
    comments = relationship('Comment', backref='user', lazy=True)
    likes = relationship('Like', backref='user', lazy=True)
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if not self.avatar:
            self.avatar = hash_avatar_url(email=self.email)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        return self.role == RoleEnum.ADMIN
    
    def full_name(self):
        return f"{self.last_name} {self.first_name}" if self.last_name and self.first_name else "-- Empty --"

    def __str__(self):
        return self.username


class Category(BaseModel):
    name = Column(String(50), nullable=True)
    books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


book_tag = db.Table('book_tag',
                    Column('book_id', ForeignKey('book.id'), nullable=False, primary_key=True),
                    Column('tag_id', ForeignKey('tag.id'), nullable=False, primary_key=True))


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return f"#{self.name}"


class Book(BaseModel):
    title = Column(String(80), unique=True)
    price = Column(Float, default=0.00)
    image = Column(Text)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey(Category.id))
    tags = relationship('Tag', secondary='book_tag', backref='books', lazy=True)
    comments = relationship('Comment', backref='book', lazy=True)
    likes = relationship('Like', backref='book', lazy=True)
    
    def __str__(self):
        return self.title
    

class Interaction(BaseModel):
    __abstract__ = True
    
    book_id = Column(Integer, ForeignKey(Book.id))
    user_id = Column(Integer, ForeignKey(User.id))


class Comment(Interaction):
    content = Column(Text)

    def __str__(self):
        return f'{self.content[:20]}...'
    

class Like(Interaction):
    def __str__(self):
        return self.active
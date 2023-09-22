import sqlalchemy
import re 
from sqlalchemy import CheckConstraint
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates


connection_string = "sqlite:///database.db"   # for SQLite, local file
db   = create_engine(connection_string)
base = declarative_base()

from sqlalchemy.orm import validates

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 
    @validates('authors','same name')
    def validate_authors(self,key,author):
        if 'name' not in author:
            raise ValueError
    @validates('phone number')
    def validate_phone_number(self,key,phone_number):
        if 'ten digits' not in phone_number:
            raise  ValueError


    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 
    @validates('posts')
    def validate_posts(self,key,posts):
        if 'title'not in posts:
            return ValueError
    @validates('post content')
    def validate_post_content(self,key,post_content):
        if 'atleast 250 characters' not in post_content:
            return ValueError
    @validates('Post summary')
    def validate_post_summary(self,key,post_summary):
        if 'maximum of 250 characters'not in post_summary:
            return ValueError
        
    VALID_CATEGORIES = ["Fiction", "Non-Fiction"]

    @validates('category')
    def validate_category(self, key, valid_category):
        if 'value' not in valid_category:
            raise ValueError("Invalid category")
        return ValueError


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())



    @validates('title')
    def validate_title(self, key, value):
        clickbait_keywords = [
            "Won't Believe",
            "Secret",
            r"Top \d+",
            "Guess"
        ]

        pattern = "|".join(clickbait_keywords)
        if not re.search(pattern, value):
            raise ValueError("Title is not sufficiently clickbait-y")
        return value
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

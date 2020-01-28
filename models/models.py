from datetime import datetime
from pytweet.database import db
from flask_login import UserMixin

class User(UserMixin,db.Model):

  __tablename__ = "users"

  id = db.Column(db.Integer,primary_key = True)
  fullname  = db.Column(db.String(255),nullable = False)
  username = db.Column(db.String(255),nullable = False)    #nullable=空白
  password = db.Column(db.String(255),nullable = False)
  # sessionのところ
  posts = db.relationship('Post',backref='author',lazy=True)  #profileの

  created_at = db.Column(db.DateTime,nullable = False,default=datetime.now)
  updated_at = db.Column(db.DateTime,nullable = False,default=datetime.now,onupdate=datetime.now)

  def __init__(self,fullname,username,password):
    self.fullname = fullname
    self.username = username
    self.password = password

  def is_active(self):
    return True
  def is_authenticated(self):
    return True

# ここで与えた箱(左辺)の名前が基準
class Profile(db.Model):
  
  __tablename__ = "profile"
  id = db.Column(db.Integer,primary_key = True)
  user_id = db.Column(db.Integer,db.ForeignKey('users.id') ,nullable = False)
  first_name = db.Column(db.String(255),nullable = False)
  last_name = db.Column(db.String(255),nullable = False)
  address = db.Column(db.String(255),nullable = False)
  occupation = db.Column(db.String(255),nullable = False)
  birthday = db.Column(db.String(255),nullable = False)
  skills = db.Column(db.String(255),nullable = False)
  created_at = db.Column(db.DateTime,nullable = False,default=datetime.now)
  updated_at = db.Column(db.DateTime,nullable = False,default=datetime.now,onupdate=datetime.now)





class Post(db.Model):
  __tablename__ = "post"

  id = db.Column(db.Integer,primary_key = True)
  # sessionのところ
  user_id = db.Column(db.Integer,db.ForeignKey('users.id') ,nullable = False)
  comments = db.relationship('Comments',backref="post",lazy=True)    # commentを１つだけ表示のため
  post = db.Column(db.String(1000),nullable = False)
  created_at = db.Column(db.DateTime,nullable = False,default=datetime.now)
  updated_at = db.Column(db.DateTime,nullable = False,default=datetime.now,onupdate=datetime.now)


class Comments(db.Model):
  __tablename__ = "comments"

  id = db.Column(db.Integer,primary_key = True)
  user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
  post_id = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)   # commentを１つだけ表示のため
  comment = db.Column(db.String(1000),nullable = False)
  created_at = db.Column(db.DateTime,nullable = False,default=datetime.now)
  updated_at = db.Column(db.DateTime,nullable = False,default=datetime.now,onupdate=datetime.now)



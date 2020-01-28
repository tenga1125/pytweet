# yamazakitenga@MacBook-Pro-od-TENGA FlaskBasic % export FLASK_APP=app.py     
# yamazakitenga@MacBook-Pro-od-TENGA FlaskBasic % export FLASK_ENV=development
# yamazakitenga@MacBook-Pro-od-TENGA FlaskBasic % flask run 

from flask import Flask,render_template,request,redirect,flash,session
from .app import app
from .database import db
import os
from .models.models import User,Profile,Post,Comments       # SQL tableに追加する
from flask_login import login_user,LoginManager,login_required,current_user,logout_user
login_manager = LoginManager()
login_manager.init_app(app)

# app = Flask(__name__)
# app.secret_key = os.urandom(24)

# pythonとつなげる
@app.route("/",methods=["GET","POST"])
def index():
  if request.method == "POST":
    user = User.query.filter_by(username=request.form["email"]).first()
    if user is not None and request.form["email"] == user.username and request.form["password"] == user.password :
      # session["user"] = user.id
      login_user(user)
      return redirect("/dashboard")
    else:
      flash(u"Invalid Username or password","error")
      flash(u"Check your input Username or password")
      return redirect("/")
      # return redirect("/contacts")       
  return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
  if request.method == "POST":
    user = User(fullname=request.form["fullname"],
                username=request.form["email"],
                password=request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect("/")      
  return render_template("register.html")


@app.route("/about",methods=["GET","POST"])     # GETとPOSTのどっちかで送るよ
@login_required
def about():
  if request.method == "POST":
    # 行き機能（html→DB（データを送信））
    profile = Profile(user_id=current_user.id,
                first_name=request.form["first_name"],          # 左辺（青文字）はDBに渡す、右辺（オレンジ文字）はhtmlに渡す
                last_name=request.form["last_name"],            # ※ 箱（変数）は models の 左辺と同じにする
                address=request.form["address"],                # ※ 右辺（html）はmodelsの左辺と同じ名前
                occupation=request.form["occupation"],
                birthday=request.form["birthday"],
                skills=request.form["skills"]
                )
    db.session.add(profile)
    db.session.commit()
    return redirect("/profile")      
  return render_template("profile.html")


@app.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
  title="Dashboard Page"
  return render_template("dashboard.html",title=title)


@app.route("/tweet",methods=["POST"])
@login_required      #ページとばない
def tweet():
  post = Post(user_id=current_user.id,post=request.form["post"])
  db.session.add(post)
  db.session.commit()
  return redirect("/profile")

@app.route("/comment",methods=["POST"])
@login_required  
def comment():
  # if request.method = "POST":
    comment = Comments(
      user_id = request.form["id"],
      comment = request.form["comment"],      #tableの中のcommentをとってくる
      post_id = request.form["id"],
      )
    db.session.add(comment)
    db.session.commit()
    return redirect("/profile")


@app.route("/contacts",methods=["GET","POST"])
# @login_required
def contacts():
  title="Contacts"
  # if request.method == "POST":
  users = User.query.all()
  return render_template("contacts/contacts.html",users=users)


@app.route("/viewprofile/<int:id>")
def viewprofile(id):
  user = User.query.filter_by(id=id).first()
  posts = Post.query.order_by(Post.created_at.desc()).all()
  profile = Profile.query.filter_by(user_id=id).first()
  return render_template("profile/profile.html",user=user,posts=posts,profile=profile)




@app.route("/profile",methods=["GET","POST"])
@login_required
def profile():
  title="Tweet Page"
  # if "user" in session:
  if current_user:
    # 帰りの機能（DB→htmlにデータを返す（画面に表示））
    posts = Post.query.order_by(Post.created_at.desc()).all()             # Classの名前と一致させる
    profile = Profile.query.filter_by(id=current_user.id).first()
    user = User.query.filter_by(id=current_user.id).first()
    # profilesの役割 : htmlの {% for profile in profiles %} の右側
    comment = Comments.query.order_by(Comments.created_at.desc()).all()   # query(命令)  order_by(順番)
    #htmlにデータをreturn：左辺（青）→fanctionの箱、右辺（白）→上の変数（左辺（箱））
    return render_template("profile/profile.html",title=title,posts=posts,profile=profile,comments=comment,user=user)
  return redirect("/")



@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect("/")

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))



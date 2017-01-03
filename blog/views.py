from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, UserMixin, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from . import app
from .database import session, Entry, User

PAGINATE_BY = 5

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )
    
@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")
    
@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user,
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))

@app.route("/entry/<id>", methods=["GET"])
def entry_detail_get(id):
    entry=session.query(Entry).filter(Entry.id==id)
    entry=entry.one()
 
    return render_template("single_entry.html",
        entry=entry,
        id=id)

@app.route("/entry/<id>/edit", methods=["GET"])
@login_required
def edit_entry(id):
    entry=session.query(Entry).filter(Entry.id==id)
    entry=entry.one()
    return render_template("edit_entry.html",
        entry=entry,
        id=id)

@app.route("/entry/<id>/edit", methods=["POST"])
@login_required
def edit_entry_post(id):
 
    entry=session.query(Entry).filter(Entry.id==id).update(\
            {"title": request.form["title"],\
            "content": request.form["content"]})
        
    session.commit()
    return redirect(url_for("entries"))

@app.route("/entry/<id>/delete", methods=["GET"])
@login_required
def delete_entry(id):
    entry=session.query(Entry).filter(Entry.id==id)
    entry=entry.one()
    return render_template("delete_entry.html",
        entry=entry,
        id=id)

@app.route("/entry/<id>/delete", methods=["POST"])
@login_required
def delete_entry_post(id):
    entry=session.query(Entry).filter(Entry.id==id).delete()

    session.commit()
    return redirect(url_for("entries"))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("entries"))

@app.route("/newuser", methods=["GET"])
@login_required
def newuser():
    return render_template("newuser.html")

@app.route("/newuser", methods=["POST"])
@login_required
def newuser_post():
    user = User(
        name = request.form["name"],
        email = request.form["email"],
        password = request.form["password"]
        )

    session.add(user)
    session.commit()
    return redirect(url_for("entries"))

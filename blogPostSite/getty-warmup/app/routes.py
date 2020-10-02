from __future__ import print_function
import sys
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import sqlalchemy

from app import app, db

from app.forms import PostForm, SortForm
from app.models import Post, Tag, postTags


@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Tag.query.count() == 0:
        tags = ['funny', 'inspiring', 'true-story', 'heartwarming', 'friendship']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    number_of_smiles = Post.query.count()
    sortform = SortForm()
    if sortform.validate_on_submit():
        sort_id = int(sortform.sort_by.data)
        if sort_id == 4: # date
            posts = Post.query.order_by(Post.timestamp.desc())
        elif sort_id == 3: # title
            posts = Post.query.order_by(Post.title.asc())
        elif sort_id == 2: # num likes
            posts = Post.query.order_by(Post.likes.desc())
        else: # happiness level
            posts = Post.query.order_by(Post.happiness_level.desc())
        return render_template('index.html', title="Smile Portal", posts=posts.all(), number_of_smiles=number_of_smiles, sort=sortform)
    
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title="Smile Portal", posts=posts.all(), number_of_smiles=number_of_smiles, sort=sortform)


@app.route('/postsmile', methods=['GET', 'POST'])
def postsmile():
    form = PostForm(csrf_enabled=True)
    if request.method == 'POST':
        if form.validate_on_submit():
            p = Post(title=request.form['title'], body=request.form['body'],
                     happiness_level=request.form['happiness_level'])
            for tag in form.tag.data:  # Appends all tags to post form.
                p.tags.append(tag)
            db.session.add(p)
            db.session.commit()
            flash('Posted!')
            return redirect(url_for('index'))
        else:
            flash('All fields were not entered', 'error')
    return render_template('create.html', form=form)


@app.route('/likepost/<post_id>', methods=['GET'])
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post.likes += 1
    db.session.commit()
    return redirect(url_for('index'))

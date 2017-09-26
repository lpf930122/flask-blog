import flask
from flask import render_template, redirect, url_for, abort, current_app, Response, request
from . import article
from .forms import PostForm
from flask_login import current_user
from .. import db
from ..models import Post, Tag
import os

#文件名合法性验证
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@article.route('/edit', methods=['GET', 'POST'])
def editpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object(), hide=form.hide.data)
        db.session.add(post)
        tags = str(form.tag.data).split()
        for i in tags:
            tag = Tag(tag=i, post_id=Post.query.filter_by(title=form.title.data).first().id)
            db.session.add(tag)
        return redirect(url_for('.post'))
    return render_template('article/edit.html', form=form)


@article.route('/entry', methods=['GET', 'POST'])
def post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POST_PER_PAGE'],
                                                                              error_out=True)
    posts = pagination.items
    tag_all = Tag.query.all()
    tagall = [i.tag for i in tag_all]
    tags = set(tagall)
    return render_template('article/posts.html', posts=posts, pagination=pagination, tags=tags, tagsall=tag_all, tagsalllist=tagall)


@article.route('/entry/<postnum>', methods=['GET', 'POST'])
def entry(postnum):
    post = Post.query.filter_by(id=postnum).first()
    if post is None:
        abort(404)
    return render_template('article/post.html', post=post)

@article.route('/upload', methods=['POST'])
def GetImage():
    file = flask.request.files['upload-file']
    if file == None:
        result = r"error|未成功获取文件，上传失败"
        res = Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            imgUrl = "http://localhost:5000" + "/static/upload/" + filename
            res = Response(imgUrl)
            res.headers["ContentType"] = "text/html"
            res.headers["Charset"] = "utf-8"
            return res
from flask import render_template, redirect, url_for, flash, current_app, request
from . import main
from ..models import User, Comment
from flask_login import login_user, current_user
from .forms import LgForm, CommentForm, ReplyForm
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = LgForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('home.html', form=form)


@main.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm()
    reply_form = ReplyForm()
    if reply_form.validate_on_submit():
        message = Comment(body=reply_form.body.data,
                          author=current_user._get_current_object(),
                          path=reply_form.commentPath.data + str(Comment.query.count() + 1))
        db.session.add(message)
        return redirect(url_for('.comment'))
    elif form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          author=current_user._get_current_object(),
                          path=str(Comment.query.count() + 1) + '/')
        db.session.add(comment)
        return redirect(url_for('.comment'))
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter(Comment.path.like('%/')).order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENT_PER_PAGE'], error_out=True)
    comments = pagination.items
    message_reply = Comment.query.filter(~Comment.path.like('%/'))
    return render_template('comment.html',
                           form=form, CommentList=comments,
                           pagination=pagination, reply_form=reply_form,
                           message_reply=message_reply, Comment=Comment)

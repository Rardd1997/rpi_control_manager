from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm
from app.model.forms import get_models_form
from app.models import WebUser
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())
    g.models_form = get_models_form()


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return render_template("index.html", title=current_app.config['WEB_NAME'])


@bp.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    user = WebUser.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)


@bp.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('You changes have been saved!'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route("/users_list")
@login_required
def users_list():
    page = request.args.get("page", 1, type=int)
    users = WebUser.query.paginate(page, current_app.config["USERS_PER_PAGE"], False)
    next_url = url_for("users_list", page=users.next_num) if users.has_next else None
    prev_url = url_for("users_list", page=users.prev_num) if users.has_prev else None
    return render_template("users_list.html", title="All Users",
                           users=users.items, next_url=next_url, prev_url=prev_url)
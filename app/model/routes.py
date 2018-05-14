from flask import render_template, redirect, url_for, \
    request, g, flash
from app import db
from flask_babel import _
from app.model import bp
from app.models import WebUser, WebRole, DefaultParam, InputParam, \
    Param, User, UserAuthorize, TimeZone, Holiday, MultiCardOpen, Event, \
    InOutFun, FirstCard
from app.model.forms import DefaultParamForm, ParamForm, InputParamForm, \
    UserForm, UserAuthorizeForm, TimeZoneForm, HolidayForm, MultiCardOpenForm, \
    EventForm, InOutFunForm, FirstCardForm, DeleteModelItemForm
from flask_login import login_required


@bp.route("/view_model/<form_html_name>", methods=["POST", "GET"])
@login_required
def view_model(form_html_name):
    form = g.models_form[form_html_name]
    model = globals()[form.model_name]
    items = model.query.all()
    if form.model_name == 'DefaultParam':
        item = model.query.first_or_404()
        fields = form.get_fields_per_rows()
        return render_template("model/default_view.html", item=item, form=form, fields=fields)
    return render_template("model/view_model.html", items=items, form=form)


@bp.route("/add_model/<form_html_name>", methods=["POST", "GET"])
@login_required
def add_model(form_html_name):
    form = g.models_form[form_html_name]
    all_fields = form.get_fields_per_rows()
    if form.validate_on_submit():
        model = globals()[form.model_name]
        fields = form.get_fields()
        model = model()
        for field in fields:
            form_attr = getattr(form, field)
            setattr(model, field, form_attr.data)
        db.session.add(model)
        db.session.commit()
        flash(_('Congratulations, new "{}" was successfully added!'.format(form.title)))
        return redirect(url_for('model.view_model', form_html_name=form_html_name))
    return render_template('model/modify_model.html', form=form, fields=all_fields)


@bp.route("/update_model/<form_html_name>/<id>", methods=["POST", "GET"])
@login_required
def update_model(form_html_name, id):
    form = g.models_form[form_html_name]
    model = globals()[form.model_name]
    model_for_update = model.query.get(int(id))
    fields = form.get_fields()
    fields_per_rows = form.get_fields_per_rows()
    if request.method == "GET":
        for field in fields:
            model_attr = getattr(model_for_update, field)
            data_attr = getattr(form, field)
            data_attr.data = model_attr
    if form.validate_on_submit():
        for field in fields:
            form_attr = getattr(form, field)
            setattr(model_for_update, field, form_attr.data)
        db.session.commit()
        flash(_('Congratulations, "{}" was successfully updated!'.format(form.title)))
        return redirect(url_for('model.view_model', form_html_name=form_html_name))
    return render_template('model/modify_model.html', form=form, fields=fields_per_rows)


@bp.route("/delete_model/<form_html_name>/<id>", methods=["POST", "GET"])
@login_required
def delete_model(form_html_name, id):
    form = DeleteModelItemForm()
    if form.validate_on_submit():
        admin_user = WebUser.query.filter_by(username='admin').first()
        if admin_user is None or not admin_user.check_password(form.password.data):
            flash(_('Invalid admin password'))
            return redirect(url_for('model.delete_model', form_html_name=form_html_name, id=id))
        model_form = g.models_form[form_html_name]
        model = globals()[model_form.model_name]
        model = model.query.get(int(id))
        db.session.delete(model)
        db.session.commit()
        flash(_('Congratulations, "{}" was successfully deleted!'.format(model_form.title)))
        return redirect(url_for('model.view_model', form_html_name=form_html_name))
    return render_template('model/delete_model.html', form=form)

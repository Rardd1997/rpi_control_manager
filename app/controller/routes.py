from _datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.controller import i2c
from app.controller import bp
from app.controller.forms import *
from flask_login import login_required
from app.models import Param


@bp.route("/close_door", methods=["GET", "POST"])
@login_required
def close_door():
    form = CloseDoorForm()
    if form.validate_on_submit():
        i2c.close_door(form.door_num.data)
        return redirect(url_for(form.form_name))
    return render_template("controller/{}.html".format(form.html_name), form=form)


@bp.route("/open_door", methods=["GET", "POST"])
@login_required
def open_door():
    form = OpenDoorForm()
    if form.validate_on_submit():
        i2c.open_door(form.door_num.data)
        return redirect(url_for(form.form_name))
    return render_template("controller/{}.html".format(form.html_name), form=form)


@bp.route("/open_door_reader", methods=["GET", "POST"])
@login_required
def open_door_reader():
    form = OpenDoorReaderForm()
    if form.validate_on_submit():
        time_to_open = Param.query.filter_by(door_num=form.door_num.data).first().open_lock_time
        i2c.open_door_reader(form.card_num.data, form.door_num.data, time_to_open)
        return redirect(url_for(form.form_name))
    return render_template("controller/{}.html".format(form.html_name), form=form)


@bp.route("/pin_status", methods=["GET", "POST"])
@login_required
def pin_status():
    form = PinStatusForm()
    if form.validate_on_submit():
        try:
            pin = int(form.pin_num.data)
            #GPIO.setup(pin, GPIO.IN)
            if True:#GPIO.input(pin):
                status = "Pin number {} is high!".format(str(pin))
            else:
                status = "Pin number {} is low!".format(str(pin))
        except:
            status = "There was an error reading pin {}.".format(str(pin))

        response_data = {
            "title": "Status of Pin({})".format(str(pin)),
            "status": status,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        return render_template("{}.html".format(form.html_name), form=form, **response_data)
    return render_template("{}.html".format(form.html_name), form=form)


@bp.route("/change/<change_pin>/<action>")
@login_required
def change_pin(change_pin, action):
    change_pin = int(change_pin)
    if action == "on":
        GPIO.output(change_pin, GPIO.HIGH)
    if action == "off":
        GPIO.output(change_pin, GPIO.HIGH)
    if action == "toggle":
        GPIO.output(change_pin, not GPIO.input(change_pin))
    return redirect("pin_status", change_pin)

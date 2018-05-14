from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


@login.user_loader
def load_user(user_id):
    return WebUser.query.get(int(user_id))


class WebUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, db.ForeignKey("web_role.id"))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    about_me = db.Column(db.String(140))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])["reset_password"]
        except:
            return
        return WebUser.query.get(int(id))


class WebRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), index=True, unique=True)


class DefaultParam(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), index=True, unique=True)
    ip_addr = db.Column(db.String(45))
    ip_mask = db.Column(db.String(45))
    id_gate = db.Column(db.String(45))
    dns_addr = db.Column(db.String(45))
    dhcp = db.Column(db.Integer)
    com_port = db.Column(db.String(45))
    com_user = db.Column(db.String(45))
    com_pass = db.Column(db.String(45))
    web_port = db.Column(db.String(45))
    base_mode = db.Column(db.Integer)
    web_user = db.Column(db.String(45))
    web_pass = db.Column(db.String(45))
    version = db.Column(db.String(45))
    ntp_server = db.Column(db.String(45))
    timezone = db.Column(db.Integer, db.ForeignKey("time_zone.rec_id"))
    time_sinc_period = db.Column(db.Integer)
    summer_time = db.Column(db.Integer)
    summer_time_start = db.Column(db.Date)
    summer_time_end = db.Column(db.Date)
    apb_sync = db.Column(db.Integer)


class Param(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.Integer, index=True, unique=True)
    door_mode = db.Column(db.Integer)
    open_lock_time = db.Column(db.Integer)
    enter_verify_time = db.Column(db.Integer)
    verify_time = db.Column(db.Integer)
    open_alarm_time = db.Column(db.Integer)
    enter_verify_mode = db.Column(db.Integer)
    exit_verify_mode = db.Column(db.Integer)
    duress_pass = db.Column(db.String(45))
    emergency_pass = db.Column(db.String(45))
    pass_mode = db.Column(db.Integer)


class InputParam(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    input_num = db.Column(db.String(45), index=True, unique=True)
    mode = db.Column(db.Integer)


class User(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.Integer, index=True, unique=True)
    card_num = db.Column(db.String(45), index=True, unique=True)
    pin_code = db.Column(db.Integer)
    group = db.Column(db.Integer)
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)


class UserAuthorize(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.Integer, db.ForeignKey("user.pin"))
    door_num = db.Column(db.Integer, db.ForeignKey("param.door_num"))
    time_zone_num = db.Column(db.Integer, db.ForeignKey("time_zone.rec_id"))
    pass_mode = db.Column(db.Integer)
    in_out = db.Column(db.Integer)


class TimeZone(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    time_zone_num = db.Column(db.String(45), index=True, unique=True)
    sun_time = db.Column(db.Integer)
    mon_time = db.Column(db.Integer)
    tue_time = db.Column(db.Integer)
    wed_time = db.Column(db.Integer)
    thu_time = db.Column(db.Integer)
    fri_time = db.Column(db.Integer)
    sut_time = db.Column(db.Integer)
    hol_time = db.Column(db.Integer)


class Holiday(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    holiday = db.Column(db.Date)
    holiday_type = db.Column(db.Integer)
    loop = db.Column(db.Integer)


class MultiCardOpen(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.Integer, db.ForeignKey("param.door_num"))
    group_num = db.Column(db.Integer)


class Event(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    event_num = db.Column(db.Integer, index=True, unique=True)
    card_num = db.Column(db.String(45), db.ForeignKey("user.card_num"))
    pin = db.Column(db.Integer, db.ForeignKey("user.pin"))
    door_num = db.Column(db.Integer, db.ForeignKey("param.door_num"))
    in_out_state = db.Column(db.Integer)
    time_second = db.Column(db.String(45))
    priority = db.Column(db.Integer)
    transmitted = db.Column(db.Integer)


class InOutFun(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, index=True, unique=True)
    time_zone_num = db.Column(db.Integer, db.ForeignKey("time_zone.rec_id"))
    event_num = db.Column(db.Integer, db.ForeignKey("event.event_num"))
    input_num = db.Column(db.String(45), db.ForeignKey("input_param.input_num"))
    out_type = db.column(db.Integer)
    out_addr = db.column(db.Integer)
    out_time = db.column(db.Integer)
    delay = db.column(db.Integer)


class FirstCard(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.Integer, db.ForeignKey("user.pin"))
    door_num = db.Column(db.Integer, db.ForeignKey("param.door_num"))
    time_zone_num = db.Column(db.Integer, db.ForeignKey("time_zone.rec_id"))

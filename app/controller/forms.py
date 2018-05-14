from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import _
from app.models import Param


class OpenDoorForm(FlaskForm):
    form_name = "open_door"
    title = _("Open door")
    description = _("Opening selected door")
    html_name = form_name

    door_num = SelectField(_("Door number"))
    submit = SubmitField(_("Open"))

    def __init__(self, *args, **kwargs):
        super(OpenDoorForm, self).__init__(*args, **kwargs)

        self.door_num.choices = []
        for item in Param.query.all():
            self.door_num.choices.append((str(item.door_num), item.door_num))


class CloseDoorForm(FlaskForm):
    form_name = "close_door"
    title = _("Close door")
    description = _("Closing selected door")
    html_name = form_name

    door_num = SelectField(_("Door number"))
    submit = SubmitField(_("Close"))

    def __init__(self, *args, **kwargs):
        super(CloseDoorForm, self).__init__(*args, **kwargs)

        self.door_num.choices = []
        for item in Param.query.all():
            self.door_num.choices.append((str(item.door_num), item.door_num))


class OpenDoorReaderForm(FlaskForm):
    form_name = "open_door_reader"
    title = _("Read card")
    description = _("Reading card for opening door")
    html_name = form_name

    card_num = StringField(_("Card number"), validators=[DataRequired()])
    door_num = SelectField(_("Door number"))
    submit = SubmitField(_("Read"))

    def __init__(self, *args, **kwargs):
        super(OpenDoorReaderForm, self).__init__(*args, **kwargs)

        self.door_num.choices = []
        for item in Param.query.all():
            self.door_num.choices.append((str(item.door_num), item.door_num))


pins = [7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40]


class PinStatusForm(FlaskForm):
    form_name = "pin_status"
    title = "Pin status"
    description = "Showing pin status"
    html_name = form_name

    pin_num = SelectField("Pin number")
    submit = SubmitField("Show")

    def __init__(self, *args, **kwargs):
        super(PinStatusForm, self).__init__(*args, **kwargs)

        self.pin_num.choices = []
        for item in pins:
            self.pin_num.choices.append((item, item))
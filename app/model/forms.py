from flask import flash, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, IPAddress, ValidationError, Length
from wtforms.fields.html5 import IntegerField, DateField
from app.model.enums import BaseParamDHCPEnum, BaseParamSummerTimeEnum, \
    BaseParamApbSyncEnum, BaseParamBaseModeEnum, ParamEnterVerifyModeEnum, \
    ParamPassModeEnum, InputParamModeEnum, InputParamNumEnum, \
    UserAuthorizeInOutEnum, UserAuthorizePassModeEnum, HolidayLoopEnum, \
    EventPriorityEnum, EventTransmittedEnum, EventInOutStateEnum, InOutFunOutTypeEnum
from app.models import User, Param, TimeZone, Event, InputParam
from flask_babel import _
import inspect


class FormHelperMixin(object):
    description_attrubites = ['form_name', 'title', 'description',
                              'model_name', 'html_name', 'meta', 'csrf_token',
                              'submit']

    @classmethod
    def get_fields_per_rows(cls):
        result_list = []
        inner_list = []
        counter = 0
        fields = cls.get_fields()
        for item in fields:
            inner_list.append(item)
            counter += 1
            if len(inner_list) == current_app.config['FIELD_PER_ROWS'] \
                    or counter == len(fields):
                result_list.append(inner_list)
                inner_list = []
        return result_list

    @classmethod
    def get_fields(cls):
        result_list = []
        for attr in cls.__dict__.keys():
            if attr not in FormHelperMixin.description_attrubites and \
                    not attr.startswith('_') and not callable(getattr(cls, attr)) \
                    and not inspect.ismethod(attr):
                result_list.append(attr)
        return result_list

    @classmethod
    def get_view_record(cls, model_item):
        ret = ''
        for field in cls.get_fields():
            label = getattr(cls, field).args[0]
            data = str(getattr(model_item, field))
            ret += label + ': ' + data + '; '
        return ret


class DefaultParamForm(FormHelperMixin, FlaskForm):
    form_name = 'DefaultParamForm'
    title = 'Default parameters'
    description = 'Table for setting global control parameters'
    model_name = 'DefaultParam'
    html_name = 'default_param'

    name = StringField('Controller name', validators=[DataRequired()])
    ip_addr = StringField('Network address', validators=[IPAddress()])
    ip_mask = StringField('MAC address', validators=[DataRequired()])
    id_gate = StringField('Gateway address', validators=[DataRequired()])
    dns_addr = StringField('DHCP Address', validators=[DataRequired()])
    dhcp = SelectField('DHCP')
    com_port = StringField('Network Port', validators=[DataRequired()])
    com_user = StringField('Network User', validators=[DataRequired()])
    com_pass = StringField('Network Password', validators=[DataRequired()])
    web_port = StringField('Web Port', validators=[DataRequired()])
    base_mode = SelectField('Base Mode')
    web_user = StringField('Web User', validators=[DataRequired()])
    web_pass = StringField('Web Password', validators=[DataRequired()])
    version = StringField('Version', validators=[DataRequired()])
    ntp_server = StringField('NTP Server')
    timezone = SelectField('Time Zone')
    time_sinc_period = IntegerField('Time Synchronize Period')
    summer_time = SelectField('Summer Time')
    summer_time_start = DateField('Summer Time Start')
    summer_time_end = DateField('Summer Time End')
    apb_sync = SelectField('APB Synchronize')

    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        super(DefaultParamForm, self).__init__(*args, **kwargs)

        self.dhcp.choices = []
        for item_name, item_value in BaseParamDHCPEnum.__members__.items():
            self.dhcp.choices.append((str(item_value.value), item_name))
        self.summer_time.choices = []
        for item_name, item_value in BaseParamSummerTimeEnum.__members__.items():
            self.summer_time.choices.append((str(item_value.value), item_name))
        self.apb_sync.choices = []
        for item_name, item_value in BaseParamApbSyncEnum.__members__.items():
            self.apb_sync.choices.append((str(item_value.value), item_name))
        self.base_mode.choices = []
        for item_name, item_value in BaseParamBaseModeEnum.__members__.items():
            self.base_mode.choices.append((str(item_value.value), item_name))
        self.timezone.choices = []
        for item in TimeZone.query.all():
            self.timezone.choices.append((str(item.rec_id), item.time_zone_num))


class ParamForm(FormHelperMixin, FlaskForm):
    form_name = 'ParamForm'
    title = 'Parameters table'
    description = 'Table for setting some parameters'
    model_name = 'Param'
    html_name = 'param'

    door_num = IntegerField('Door number')
    door_mode = IntegerField('Door mode')
    open_lock_time = IntegerField('Open lock time')
    enter_verify_time = IntegerField('Enter verify time')
    verify_time = IntegerField('Verify time')
    open_alarm_time = IntegerField('Open alarm time')
    enter_verify_mode = SelectField('Enter verify mode')
    exit_verify_mode = SelectField('Exit verify mode')
    duress_pass = StringField('Dures password', validators=[Length(min=0, max=8)])
    emergency_pass = StringField('Emergency password')
    pass_mode = SelectField('Pass mode')

    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        super(ParamForm, self).__init__(*args, **kwargs)

        self.enter_verify_mode.choices = []
        for name, value in ParamEnterVerifyModeEnum.__members__.items():
            self.enter_verify_mode.choices.append((str(value.value), name))

        self.exit_verify_mode.choices = []
        for name, value in ParamEnterVerifyModeEnum.__members__.items():
            self.exit_verify_mode.choices.append((str(value.value), name))

        self.pass_mode.choices = []
        for name, value in ParamPassModeEnum.__members__.items():
            self.pass_mode.choices.append((str(value.value), name))

    def validate_enter_verify_time(self, enter_verify_time):
        if not (self.open_lock_time.data > enter_verify_time.data):
            error = 'Enter-verify time must be less than open-lock time'
            flash(error)
            raise ValidationError(error)


class InputParamForm(FormHelperMixin, FlaskForm):
    form_name = 'InputParamForm'
    title = 'Input parameters'
    description = 'Table for setting input parameters'
    model_name = 'InputParam'
    html_name = 'input_param'

    input_num = SelectField('Input number')
    mode = SelectField('Mode')

    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        super(InputParamForm, self).__init__(*args, **kwargs)

        self.input_num.choices = []
        for name, value in InputParamNumEnum.__members__.items():
            self.input_num.choices.append((str(value.value), name))
        self.mode.choices = []
        for name, value in InputParamModeEnum.__members__.items():
            self.mode.choices.append((str(value.value), name))


class UserForm(FormHelperMixin, FlaskForm):
    form_name = 'UserForm'
    title = 'User parameters'
    description = 'Table for setting users key'
    model_name = 'User'
    html_name = 'user'

    pin = IntegerField('User Pin', validators=[DataRequired()])
    card_num = StringField('Card number', validators=[DataRequired()])
    pin_code = IntegerField('Pin code', validators=[DataRequired()])
    group = IntegerField('Group', validators=[DataRequired()])
    date_start = DateField('Start date', validators=[DataRequired()])
    date_end = DateField('End date', validators=[DataRequired()])

    submit = SubmitField(_('Submit'))

    def validate_date_start(self, date_start):
        success = True
        if self.date_end and date_start:
            success = self.date_end.data > date_start.data
        if not success:
            error = 'End datetime must be greater than start datetime'
            flash(error)
            raise ValidationError(error)


class UserAuthorizeForm(FormHelperMixin, FlaskForm):
    form_name = 'UserAuthorizeForm'
    title = 'User authorize'
    description = 'Access rights table'
    model_name = 'UserAuthorize'
    html_name = 'user_authorize'

    pin = SelectField('User Pin')
    door_num = SelectField('Door number')
    time_zone_num = SelectField('Time zone number')
    pass_mode = SelectField('Pass mode')
    in_out = SelectField('Inside/Outside')

    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        super(UserAuthorizeForm, self).__init__(*args, **kwargs)

        self.pass_mode.choices = []
        for name, value in UserAuthorizePassModeEnum.__members__.items():
            self.pass_mode.choices.append((str(value.value), name))

        self.in_out.choices = []
        for name, value in UserAuthorizeInOutEnum.__members__.items():
            self.in_out.choices.append((str(value.value), name))

        self.pin.choices = []
        for item in User.query.all():
            self.pin.choices.append((str(item.pin), item.pin))

        self.door_num.choices = []
        for item in Param.query.all():
            self.door_num.choices.append((str(item.door_num), item.door_num))

        self.time_zone_num.choices = []
        for item in TimeZone.query.all():
            self.time_zone_num.choices.append((str(item.rec_id), item.time_zone_num))


class TimeZoneForm(FormHelperMixin, FlaskForm):
    form_name = 'TimeZoneForm'
    title = 'TimeZone'
    description = 'TimeZone table'
    model_name = 'TimeZone'
    html_name = 'time_zone'

    time_zone_num = StringField('Time zone number', validators=[DataRequired()])
    sun_time = IntegerField('Sunday time')
    mon_time = IntegerField('Monday time')
    tue_time = IntegerField('Tuesday time')
    wed_time = IntegerField('Wednesday time')
    thu_time = IntegerField('Thusday time')
    fri_time = IntegerField('Friday time')
    sut_time = IntegerField('Suturday time')
    hol_time = IntegerField('Holiday time')

    submit = SubmitField(_('Submit'))


class HolidayForm(FormHelperMixin, FlaskForm):
    form_name = 'HolidayForm'
    title = 'Holiday'
    description = 'Holidays table'
    model_name = 'Holiday'
    html_name = 'holiday'

    holiday = DateField('Holiday', validators=[DataRequired()])
    holiday_type = IntegerField('Holiday type')
    loop = SelectField('Is loop?')

    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        super(HolidayForm, self).__init__(*args, **kwargs)

        self.loop.choices = []
        for name, value in HolidayLoopEnum.__members__.items():
            self.loop.choices.append((str(value.value), name))


class MultiCardOpenForm(FormHelperMixin, FlaskForm):
    form_name = 'MultiCardOpenForm'
    title = 'Multi card open'
    description = title
    model_name = 'MultiCardOpen'
    html_name = 'multi_card_open'

    door_num = SelectField('Door number')
    group_num = IntegerField('Group number')

    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        super(MultiCardOpenForm, self).__init__(*args, **kwargs)

        self.door_num.choices = []
        for item in Param.query.all():
            self.door_num.choices.append((str(item.door_num), item.door_num))


class EventForm(FormHelperMixin, FlaskForm):
    form_name = 'EventForm'
    title = 'Events table'
    description = title
    model_name = 'Event'
    html_name = 'event'

    event_num = IntegerField('Event number')
    card_num = SelectField('Card number')
    pin = SelectField('User Pin')
    door_num = SelectField('Door number')
    in_out_state = SelectField('Door number')
    time_second = StringField('Time', validators=[DataRequired()])
    priority = SelectField('Priority')
    transmitted = SelectField('Is Transmitted')

    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.in_out_state.choices = []
        for name, value in EventInOutStateEnum.__members__.items():
            self.in_out_state.choices.append((str(value.value), name))

        self.priority.choices = []
        for name, value in EventPriorityEnum.__members__.items():
            self.priority.choices.append((str(value.value), name))

        self.transmitted.choices = []
        for name, value in EventTransmittedEnum.__members__.items():
            self.transmitted.choices.append((str(value.value), name))

        self.card_num.choices = []
        self.pin.choices = []
        for item in User.query.all():
            self.card_num.choices.append((item.card_num, item.card_num))
            self.pin.choices.append((str(item.pin), item.pin))

        self.door_num.choices = []
        for item in Param.query.all():
            self.door_num.choices.append((str(item.door_num), item.door_num))


class InOutFunForm(FormHelperMixin, FlaskForm):
    form_name = 'InOutFunForm'
    title = 'Linked action table'
    description = title
    model_name = 'InOutFun'
    html_name = 'in_out_fun'

    index = IntegerField('Index', validators=[DataRequired()])
    time_zone_num = SelectField('Time zone number', validators=[DataRequired()])
    event_num = SelectField('Event number', validators=[DataRequired()])
    input_num = SelectField('Input number', validators=[DataRequired()])
    out_type = IntegerField('Out type')
    out_addr = IntegerField('Out address')
    out_time = IntegerField('Out time')
    delay = IntegerField('Delay')

    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        super(InOutFunForm, self).__init__(*args, **kwargs)

        self.out_type.choices = []
        for name, value in InOutFunOutTypeEnum.__members__.items():
            self.out_type.choices.append((str(value.value), name))

        self.time_zone_num.choices = []
        for item in TimeZone.query.all():
            self.time_zone_num.choices.append((str(item.rec_id), item.time_zone_num))

        self.event_num.choices = []
        for item in Event.query.all():
            self.event_num.choices.append((str(item.event_num), item.event_num))

        self.input_num.choices = []
        for item in InputParam.query.all():
            self.input_num.choices.append((str(item.input_num), item.input_num))


class FirstCardForm(FormHelperMixin, FlaskForm):
    form_name = 'FirstCardForm'
    title = 'First card table'
    description = 'Opening table by the first card'
    model_name = 'FirstCard'
    html_name = 'first_card'

    pin = SelectField('User Pin', validators=[DataRequired()])
    door_num = SelectField('Door number', validators=[DataRequired()])
    time_zone_num = SelectField('Time zone number', validators=[DataRequired()])

    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        super(FirstCardForm, self).__init__(*args, **kwargs)

        self.pin.choices = []
        for item in User.query.all():
            self.pin.choices.append((str(item.pin), item.pin))

        self.door_num.choices = []
        for item in Param.query.all():
            self.door_num.choices.append((str(item.door_num), item.door_num))

        self.time_zone_num.choices = []
        for item in TimeZone.query.all():
            self.time_zone_num.choices.append((str(item.rec_id), item.time_zone_num))


class DeleteModelItemForm(FlaskForm):
    title = 'Delete model item form'
    description = 'Enter admin`s account password for deleting selected model item'

    password = PasswordField('Admin password', validators=[DataRequired()])
    submit = SubmitField(_('Submit'))


def get_models_form():
    return {'default_param': DefaultParamForm(), 'param': ParamForm(), 'input_param': InputParamForm(),
            'user': UserForm(), 'user_authorize': UserAuthorizeForm(), 'time_zone': TimeZoneForm(),
            'holiday': HolidayForm(), 'multi_card_open': MultiCardOpenForm(), 'event': EventForm(),
            'in_out_fun': InOutFunForm()}

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    national_id = StringField('National ID',
                              validators=[DataRequired(), Length(8, 15)],
                              render_kw={'class': 'input'}
                              )

    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'input'})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In', render_kw={'class': 'button is-success'})

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class DoctorLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(DoctorLoginForm, self).__init__(*args, **kwargs)


class PatientLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(PatientLoginForm, self).__init__(*args, **kwargs)


class AdminLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(AdminLoginForm, self).__init__(*args, **kwargs)


class AddPatientForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired()], render_kw={'class': 'input'})
    patient_surname = StringField('Patient Surname', validators=[DataRequired()], render_kw={'class': 'input'})
    patient_gender = RadioField('Patient Gender', validators=[DataRequired()], choices=["Male", "Female", "Others"])
    patient_age = IntegerField('Patient Age', validators=[DataRequired()], render_kw={'class': 'input'})

    def __init__(self, *args, **kwargs):
        super(AddPatientForm, self).__init__(*args, **kwargs)

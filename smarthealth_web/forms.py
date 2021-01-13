from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, EqualTo


def validate_nationalid(form, field):
    if not field.data.isnumeric() or len(field.data) != 11:
        raise ValidationError("National ID format is not valid.")


class DoctorLoginForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(1, 50)],
                           render_kw={'class': 'input'}
                           )

    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'input'})
    submit = SubmitField('Log In', render_kw={'class': 'button is-success'})

    def __init__(self, *args, **kwargs):
        super(DoctorLoginForm, self).__init__(*args, **kwargs)


class PatientLoginForm(FlaskForm):

    national_id = StringField('National ID',
                              validators=[DataRequired(), Length(8, 15)],
                              render_kw={'class': 'input'}
                              )

    logcode = PasswordField('Log Code', validators=[DataRequired()], render_kw={'class': 'input'})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In', render_kw={'class': 'button is-success'})

    def __init__(self, *args, **kwargs):
        super(PatientLoginForm, self).__init__(*args, **kwargs)


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'class': 'input'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'input'})

    submit = SubmitField('Login', render_kw={'class': 'button is-success'})

    def __init__(self, *args, **kwargs):
        super(AdminLoginForm, self).__init__(*args, **kwargs)


class AddPatientForm(FlaskForm):
    patient_national_id = StringField('Patient National ID', validators=[DataRequired(), validate_nationalid], render_kw={'class': 'input'})
    patient_name = StringField('Patient Name', validators=[DataRequired()], render_kw={'class': 'input'})
    patient_surname = StringField('Patient Surname', validators=[DataRequired()], render_kw={'class': 'input'})
    patient_gender = RadioField('Patient Gender', validators=[DataRequired()], choices=["Male", "Female", "Others"])
    patient_age = IntegerField('Patient Age', validators=[DataRequired()], render_kw={'class': 'input'})

    def __init__(self, *args, **kwargs):
        super(AddPatientForm, self).__init__(*args, **kwargs)


class AddDoctorForm(FlaskForm):
    national_id = StringField('Doctor National ID', validators=[DataRequired(), validate_nationalid], render_kw={'class': 'input'})
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)], render_kw={'class': 'input'})
    surname = StringField('Surname', validators=[DataRequired(), Length(1, 30)], render_kw={'class': 'input'})
    password = PasswordField('Password',
                             validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')],
                             render_kw={'class': 'input'}
                             )
    confirm = PasswordField('Verify password', render_kw={'class': 'input'})
    username = StringField('Username', validators=[DataRequired(), Length(1, 30)], render_kw={'class': 'input'})
    hospital = StringField('Hospital', validators=[DataRequired()], render_kw={'class': 'input'})
    title = StringField('Title of the doctor', validators=[DataRequired(), Length(1, 50)], render_kw={'class': 'input'})
    profession = StringField('Profession', validators=[DataRequired(), Length(1, 50)], render_kw={'class': 'input'})

    def __init__(self, *args, **kwargs):
        super(AddDoctorForm, self).__init__(*args, **kwargs)

class UpdateAppointmentForm(FlaskForm):
    appointment_realted_patient = IntegerField('Patient ID', validators=[DataRequired()], render_kw={'class': 'input'})
    appointment_doctor_diagnosis =  StringField("Doctor's Diagnosis",  render_kw={'class': 'input'})
    appointment_diagnosis_comment = StringField('Comments', render_kw={'class': 'input'})

    def __init__(self, *args, **kwargs):
        super(UpdateAppointmentForm, self).__init__(*args, **kwargs)
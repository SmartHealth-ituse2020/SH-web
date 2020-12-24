from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class DoctorLoginForm(FlaskForm):
    national_id = StringField('National ID',
                              validators=[DataRequired(), Length(8, 15)],
                              render_kw={'class': 'input'}
                              )

    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'input'})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In', render_kw={'class': 'button is-success'})

    def __init__(self, *args, **kwargs):
        super(DoctorLoginForm, self).__init__(*args, **kwargs)

class DoctorLoginForm(FlaskForm):
    national_id = StringField('National ID',
                              validators=[DataRequired(), Length(8, 15)],
                              render_kw={'class': 'input'}
                              )

    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'input'})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In', render_kw={'class': 'button is-success'})

    def __init__(self, *args, **kwargs):
        super(DoctorLoginForm, self).__init__(*args, **kwargs)
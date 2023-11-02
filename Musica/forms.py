from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import EmailField, PasswordField, StringField, BooleanField, TextAreaField, SelectField, RadioField, FileField, SubmitField, validators
from wtforms.validators import DataRequired, ValidationError

# custom validators
def no_spaces(form,field):
    if field.data is not None and field.data.strip() == "":
        raise ValidationError('Field cannot contain only empty spaces.')

# forms

class WelcomeForm(FlaskForm):
    email_id = EmailField(label='Email',validators=[DataRequired('Email required!')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email_id = EmailField(label='Email',validators=[DataRequired('Email required!')])
    password = PasswordField(label='Password',validators=[DataRequired('Password required!')])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    email_id = EmailField(label='Email',validators=[DataRequired('Email required!')])
    f_name = StringField(label='Your name',validators=[DataRequired('Please enter your name')]);l_name = StringField(label='Last name')
    password = PasswordField('New Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

class ProfilePic(FlaskForm):
    pic = FileField(label='Profile pic',validators=[DataRequired('Select Picture!')])
    submit = SubmitField('Submit')

class BecomeCreator(FlaskForm):
    aknowledgement = BooleanField(label='I here by confirm that I\'ll follow rules for creator role and want to proceed to become a creator.',validators=[DataRequired('Check the box to proceed!')])
    submit = SubmitField('Submit')

class Upgrade(FlaskForm):
    transaction_id = StringField(label='transaction-id',validators=[DataRequired('Enter transaction id!')])
    submit = SubmitField('Submit')

language_choices = [('English'),('Foreign language'),('Hindi'),('Other'),('Telugu'),('Tamil'),('Urdu')]
genre = [('DJ'),('Love'),('Motivational'),('Romantic'),('Sad')]

class UploadSong(FlaskForm):
    file = FileField(label='Song file *(mp3)',validators=[DataRequired('Song file is required!'), FileAllowed(['mp3'], 'Only MP3 files are allowed!')])
    file_cover = FileField(label='Song cover image',validators=[FileAllowed(['jpeg','jpg','png'],'Only jpeg, jpg & png files are supported!')])
    title = StringField(label='Title',validators=[DataRequired('Song name is required!')])
    language = SelectField(label='Language',validators=[DataRequired('Select language')],choices=language_choices)
    genre = SelectField(label='Genre',validators=[DataRequired('Select genre')],choices=genre)
    submit = SubmitField('Submit')

class PlaylistCreate(FlaskForm):
    title = StringField(label='Title',validators=[DataRequired('Song name is required!')])
    submit = SubmitField('Submit')

class AlbumCreate(FlaskForm):
    title = StringField(label='Title',validators=[DataRequired('Song name is required!')])
    submit = SubmitField('Submit')

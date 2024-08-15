from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class SnippetForm(FlaskForm):
    content = TextAreaField('Snippet', validators=[DataRequired()])
    secret_key = StringField('Secret Key (Optional)', validators=[Optional()])
    submit = SubmitField('Create Shareable URL')

class DecryptForm(FlaskForm):
    secret_key = StringField('Secret Key', validators=[DataRequired()])
    submit = SubmitField('Decrypt')

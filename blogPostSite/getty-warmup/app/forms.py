from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length,Email
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.models import Post, Tag

def get_tag():
    return Tag.query

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired('Please enter a title')])
    happiness_level = SelectField('Happiness Level',
                                  choices=[(3, 'mondo epic cool'), (2, 'meh'), (1, 'sad')])
    submit = SubmitField('Post')
    body = TextAreaField('Post', validators=[DataRequired('Please enter a message to post!'),
                                             Length(min=1,
                                                    max=1500,
                                                    message='In order to post, you must enter a message with more '
                                                            'than 1 and fewer than 1500 characters!')])
    tag = QuerySelectMultipleField('Tag', query_factory=lambda: Tag.query.all(), get_label=lambda x: x.name,
                                   widget=ListWidget(prefix_label=False),
                                   option_widget=CheckboxInput())

class SortForm(FlaskForm):
    sort_by = SelectField('Sort by:', choices=[(4,'date'),(3,'title'),(2,'# of likes'),(1,'happiness level')])
    submit = SubmitField('Refresh')
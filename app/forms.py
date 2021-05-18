from app import models
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

class AddCompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    ticker = StringField('Ticker', validators=[DataRequired()])
    shares_outstanding = IntegerField('Shares Outstanding', validators=[DataRequired()])
    share_price = FloatField('Share Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddTradeForm(FlaskForm):
    shares = IntegerField('Shares', validators=[DataRequired()])
    company = QuerySelectField(
        'Company',
        query_factory=lambda: models.Company.query,
        allow_blank=False
    )
    submit = SubmitField('Submit')

from flask_wtf import Flaskform
from wtforms import StringField,IntegerField,SelectField,SubmitField
from wtforms.validators import DataRequired,NumberRange
from wtffroms_sqlalchemy.fields import QuerySelectField, SelectMultipleField, QuerySelectMultipleField
# form for customers
class customer_purchase(Flaskform):
 name =  StringField('name', validators = [DataRequired()])
# customer info, below customer can choose multiple orders
 phone_number = IntegerField('phone number', validators = [ NumberRange(min=10000000, max=10000000000), DataRequired()])
 dishes =  QuerySelectMultipleField(
    'dishes'
 )
# Qty of all dishes chosen is th same for the time bieng
 qty = IntegerField('phone number', validators = [NumberRange(min = 1, max = 4 ) ,DataRequired()])
 orderfood = SubmitField( 'Order Food')




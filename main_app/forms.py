from django.forms import ModelForm, Form, CharField, PasswordInput
from .models import LineItem

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class LineItemForm(ModelForm):
    class Meta:
        model = LineItem
        fields = ['size', 'quantity']

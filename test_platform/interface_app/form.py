from django import forms
from interface_app.models import TestCase


class TestCaseForm(forms.ModelForm):
    
    class Meta:
        model = TestCase
        fields = ['module']


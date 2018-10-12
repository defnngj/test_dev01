from django import forms


class ProjectForm(forms.Form):
    name = forms.CharField(label='名称', max_length=100)
    describe = forms.Field(label="描述")

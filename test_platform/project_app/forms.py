from django import forms
from .models import Project


# # 问题：1、如果不勾选状态怎么设置？
# class ProjectForm(forms.Form):
#     name = forms.CharField(label="名称", max_length=100)
#     describe = forms.CharField(label="描述", widget=forms.Textarea)
#     status = forms.BooleanField(label="状态")


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ['create_time']



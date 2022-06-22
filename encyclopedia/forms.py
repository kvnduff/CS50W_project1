from django import forms


# Title form
class TitleForm(forms.Form):
    title = forms.CharField(label='')


# Content form
class ContentForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea())

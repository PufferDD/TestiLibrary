from django import forms

class WorkSearchForm(forms.Form):
    query = forms.CharField(label='Search', required=False)
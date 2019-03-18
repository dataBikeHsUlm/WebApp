from django import forms

class CrowForm(forms.Form):
    from_zip = forms.CharField(max_length=5,required=True)
    from_iso = forms.CharField(max_length=2,required=True)
    to_zip = forms.CharField(max_length=5,required=True)
    to_iso = forms.CharField(max_length=2,required=True)

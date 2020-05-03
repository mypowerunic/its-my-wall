from django import forms
class Email_SendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)

from testapp.models import comment
class CommentForm(forms.ModelForm):
    class Meta:
        model=comment
        fields=('name','email','body')    

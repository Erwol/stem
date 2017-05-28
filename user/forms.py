from django import forms
from user.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirmar = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['password', 'username', 'email']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirmar = cleaned_data.get("confirmar")

        if password != confirmar:
            raise forms.ValidationError("La contraseña debe coincidir")
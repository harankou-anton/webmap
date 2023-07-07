from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())


class UploadedData(forms.Form):
    name = forms.CharField(max_length=20)
    file = forms.FileField()


class UpdateData(forms.Form):
    file = forms.FileField()

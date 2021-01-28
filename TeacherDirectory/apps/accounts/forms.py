from django.contrib.auth import authenticate, get_user_model
from django import forms

# Fetch model
User = get_user_model()


# Customize Login Form
class UserLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    # Overwrite the clean method
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("please enter valid username and password")
            if not user.check_password(password):
                raise forms.ValidationError("please enter valid password")
            if not user.is_active:
                raise forms.ValidationError("user is not active user")
        return super().clean(*args, **kwargs)
from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(required=True, max_length=30)
    email = forms.EmailField(required=True, max_length=50)
    avatar = forms.ImageField(required=True)
    password1 = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput)
    invite_code = forms.IntegerField(required=False)

    # def check_passwords(self):
    #     cleaned_data = self.cleaned_data
    #     password1 = cleaned_data.get('password1')
    #     password2 = cleaned_data.get('password2')
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError('Passwords must be equal')
    #     return cleaned_data

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                msg = 'Passwords must be equal'
                self.add_error('password1', msg)


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50)
    avatar = forms.ImageField()
    old_password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput)
    invite_code = forms.IntegerField()

    def __init__(self, user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self._user = user

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self._user.check_password(old_password):
            msg = 'Enter right password'
            self.add_error('password1', msg)
            return

        return old_password

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        old_password = self.cleaned_data.get('old_password')
        if password1 and password2 and old_password:
            if password1 != password2:
                msg = 'Passwords must be equal'
                self.add_error('password2', msg)

from django import forms
from account.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Account')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)
    fullName = forms.CharField(label='Name', max_length=128)
    website = forms.URLField(label='Personal Website', max_length=128)
    address = forms.CharField(label='Address', max_length=128)
    
    class Meta:
        model=User
        fields = ['username', 'password', 'password2', 'fullName', 'website', 'address']
        
        
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password!=password2:
            raise forms.ValidationError('Password you entered does not match')
        return password2
    
    def save(self):
        user = super().save(commit=False)
        user.set_password(user.password)
        user.save()
        return user
        
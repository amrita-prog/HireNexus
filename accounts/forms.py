from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm #username, p1, p2
import uuid #base64 unique key generator

class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password1', 'password2','resume', 'phone','profile_image']
        

    def save(self, commit=True):
        user = super().save(commit=False) # dont save
        base_username = user.email.split('@')[0] # amrita@gmail.com --> [amrita,gmail.com]
        user.username = f"{base_username}_{uuid.uuid4().hex[:4]}" # this will generate username with hexadecimal value
        user.roles = 'student'
        
        profile_image = self.cleaned_data.get('profile_image')
        resume = self.cleaned_data.get('resume')
        if commit:
            user.profile_image = None
            user.resume = None
            user.save()

            if profile_image:
                user.profile_image = profile_image

            if resume:
                user.resume = resume

            user.save(update_fields=['profile_image','resume'])
        return user
    

class RecruiterSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password1', 'password2', 'phone','profile_image']
        exclude = ['resume']

    def save(self, commit=True):
        user = super().save(commit=False)
        base_username = user.email.split('@')[0]
        user.username = f"{base_username}_{uuid.uuid4().hex[:4]}"
        user.roles = 'recruiter'
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone', 'profile_image', 'resume']

        def __int__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(ProfileEditForm,self).__init__(*args, **kwargs)
            if user and user.roles != 'student':
                self.fields.pop('resume')
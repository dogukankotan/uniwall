# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from main.models import UniwallUser, Pictures, Entry, Event


class SignUpForm(forms.ModelForm):
    school = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UniwallUser.objects.create(school=self.cleaned_data['school'], user=user)
        return user


class EntryForm(forms.Form):
    content = forms.CharField()

    def save(self, user):
        uni_user = UniwallUser.objects.get(user=user)
        Entry.objects.create(content=self.cleaned_data['content'], user=uni_user)


class PictureForm(forms.Form):
    content = forms.FileField()

    def save(self, user):
        uni_user = UniwallUser.objects.get(user=user)
        Pictures.objects.create(content=self.cleaned_data['content'], user=uni_user)


class EventForm(forms.Form):
    event_date = forms.DateField()
    event_time = forms.TimeField()
    event_content = forms.CharField()
    event_title = forms.CharField()

    def save(self, user):
        uni_user = UniwallUser.objects.get(user=user)
        Event.objects.create(date=self.cleaned_data['event_date'], time=self.cleaned_data['event_time'],
                             content=self.cleaned_data['event_content'], title=self.cleaned_data['event_title'] ,organizator=uni_user)

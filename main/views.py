# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import auth
from main.forms import SignUpForm, PictureForm, EntryForm, EventForm
from main.models import Entry, Pictures, Event, Subscribers, UniwallUser

schools = ['İstanbul Bilgi Üniversitesi', 'Sabancı Üniversitesi', 'Koç Üniversitesi', 'İstanbul Şehir Üniversitesi',
           'İstanbul Medeniyet Üniversitesi', 'İstanbul Üniversitesi', 'Marmara Üniversitesi']


def login_view(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            try:
                u = User.objects.get(email=email)
                username = u.username
                user = auth.authenticate(username=username, password=password)
            except:
                error = 'Lütfen geçerli bir e-posta giriniz'
                return render(request, 'login.html', {'error': error})
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                error = 'Kullanıcı adınız veya şifreniz yanlış'
                return render(request, 'login.html', {'error': error})  # if user logged in, no need to login again!
        return render(request, 'login.html')
    else:
        return HttpResponseRedirect('/')  # if request is get or something then redirect it to home


def register_view(request):
    if request.user.is_authenticated():  # if the user is already logged in then no need to register view
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/login')
        else:
            form = SignUpForm()
    return render(request, 'register.html', {'sc': schools, 'form': form, 'error':form.errors})


@login_required  # this decorator gives it to permission that have to login!
def index_view(request):
    entries = Entry.objects.get_uni_entries(request.user)
    pictures = Pictures.objects.get_uni_pictures(request.user)
    events = Event.objects.get_uni_events(request.user)
    share_center = UniwallUser.objects.get(user=request.user).school
    event_timetoday = datetime.today().time()
    event_datetoday = str(datetime.today().date())
    return render(request, 'index.html', locals())


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def create_entry(request):
    if request.method == 'POST':
        entry_form = EntryForm(request.POST)
        if entry_form.is_valid():
            entry_form.save(request.user)
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


@login_required
def create_picture(request):
    if request.method == 'POST':
        upload_form = PictureForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload_form.save(request.user)
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')  # if request is get or something then redirect it to home


def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save(request.user)
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def join_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        uni_user = UniwallUser.objects.get(user=request.user)
        Subscribers.objects.create(event=event, user=uni_user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def change_password(request):
    pass


def delete_event(request):
    pass


def change_event(request):
    pass


def settings_view(request):
    pass

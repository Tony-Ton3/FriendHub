from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from application.forms import JoinForm, LoginForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')

def join(request):
    # if someone submitted a join form (created account)
    if (request.method == "POST"):
        jform = JoinForm(request.POST)
        # check if form is valid
        if (jform.is_valid()):
            # save form data to DB
            user = jform.save()
            # encrypt the password
            user.set_password(user.password)
            # save encrypted password to DB
            user.save()
            # success
            return redirect("/")
        else:
            # invalid form
            page_data = { "join_form": jform }
            return render(request, 'join.html', page_data)
    else:
        # a get request, someone is trying to sign up so send them the join form
        jform = JoinForm()
        page_data = { "join_form": jform }
        return render(request, 'join.html', page_data)

def user_login(request):
    # if someone sent login form
    if (request.method == 'POST'):
        # create a LoginForm instance with sent data
        lform = LoginForm(request.POST)
        # check if form is valid
        if lform.is_valid():
            # extract the username and password from the form's cleaned data
            username = lform.cleaned_data["username"]
            password = lform.cleaned_data["password"]
            # authenticate the user
            user = authenticate(username=username, password=password)
            if user:
                # check if the user account is active
                if user.is_active:
                    # log in the user and redirect to the home page
                    login(request, user)
                    return redirect("/")
                else:
                    # return an HttpResponse indicating that the account is not active
                    return HttpResponse("This account is not active.")
            else:
                # if authentication fails, re-render the login form with an error message
                return render(request, 'login.html', {"login_form": LoginForm, "correct": False})
    else:
        # someone is trying to access the login form, so send the form
        return render(request, 'login.html', {"login_form": LoginForm, "correct": True})

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect("/")
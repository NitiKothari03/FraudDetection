import pandas as pd
from .utils import perform_fraud_detection
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

def home(request):
    return render(request, 'home.html')


def uploadDocument(request):
    if not request.user.is_authenticated:
        return redirect('loginAccount')

    if request.method == 'POST':
        uploaded_file = request.FILES['csv_file']

        if uploaded_file.name.endswith('.csv'):
            try:
                df = pd.read_csv(uploaded_file)
                analysis_results, n_outliers, outliers = perform_fraud_detection(df,
                                                            'analysisResults.html')
                return render(request, 'analysisResults.html', {
                    'results': analysis_results, 'n_outliers' : n_outliers,
                    'outliers' : outliers})
            except Exception as e:
                print(e)
                return render(request, 'uploadDoc.html',
                              {'error': 'Invalid file'})
    else:

        return render(request, 'uploadDoc.html')


def signupAccount(request):
    if request.method == 'GET':
        return render(request, 'signupAccount.html',
                      {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST[
                                                    'password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupAccount.html',
                              {'form': UserCreationForm,
                               'error': 'Username Already Exists!'})
        else:
            return render(request, 'signupAccount.html',
                          {'form': UserCreationForm,
                           'error': 'Password do not match!'})


def logoutAccount(request):
    logout(request)
    return redirect('home')


def loginAccount(request):
    if request.method == "GET":
        return render(request, 'loginAccount.html',
                      {'form': AuthenticationForm})

    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])

        if user is None:
            return render(request, 'loginAccount.html',
                          {'form': AuthenticationForm,
                           'error': 'Username/Password do not match'})
        else:
            login(request, user)
            return redirect('/')
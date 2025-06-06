from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,"home.html")
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name, last_name=last_name)
                user.save();
                print("User Created")
                return redirect('signin')
        else:
            messages.info(request, 'Password not matching..')
            return redirect('signup')
        return redirect('/')
    else:
        return render(request, 'signup.html')
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('predict')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
def predict(request):
    if (request.method == 'POST'):
        Age = int(request.POST['Age'])
        Gender = int(request.POST['Gender'])
        Air_Pollution = int(request.POST['Air Pollution'])
        Alcohol_use = int(request.POST['Alcohol use'])
        Dust_Allergy = int(request.POST['Dust Allergy'])
        OccuPational_Hazards = int(request.POST['OccuPational Hazards'])
        Genetic_Risk = int(request.POST['Genetic Risk'])
        chronic_Lung_Disease = int(request.POST['chronic Lung Disease'])
        Balanced_Diet = int(request.POST['Balanced Diet'])
        Obesity = int(request.POST['Obesity'])
        Smoking = int(request.POST['Smoking'])
        Passive_Smoker = int(request.POST['Passive Smoker'])
        Chest_Pain = int(request.POST['Chest Pain'])
        Coughing_of_Blood = int(request.POST['Coughing of Blood'])
        Fatigue = int(request.POST['Fatigue'])
        Weight_Loss = int(request.POST['Weight Loss'])
        Shortness_of_Breath = int(request.POST['Shortness of Breath'])
        Wheezing = int(request.POST['Wheezing'])
        Swallowing_Difficulty = int(request.POST['Swallowing Difficulty'])
        Clubbing_of_Finger_Nails = int(request.POST['Clubbing of Finger Nails'])
        Frequent_Cold = int(request.POST['Frequent Cold'])
        Dry_Cough = int(request.POST['Dry Cough'])
        Snoring = int(request.POST['Snoring'])
        df = pd.read_csv(r"static/dataset/lungcancer.csv")
        labels = df.columns[0:-1]
        X = df[labels]
        X = np.asarray(X, dtype='float64')
        Y = df['Level']
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=1)
        reg = LogisticRegression()
        reg.fit(X_train, Y_train)
        model = reg
        predic = np.array([[Age,Gender,Air_Pollution,Alcohol_use,Dust_Allergy,OccuPational_Hazards,Genetic_Risk,chronic_Lung_Disease ,Balanced_Diet ,Obesity,Smoking ,Passive_Smoker,Chest_Pain ,Coughing_of_Blood ,Fatigue ,Weight_Loss,Shortness_of_Breath,Wheezing,Swallowing_Difficulty,Clubbing_of_Finger_Nails,Frequent_Cold,Dry_Cough,Snoring]])
        predic.reshape(-1,1)
        pred = model.predict(predic)
        diagnosis = pred[0]
        if (diagnosis == 1):
            r = "Positive"
        elif(diagnosis == 0):
            r= "Medium"
        else:
            r = "Negative"
        messages.info(request, r)
    return render(request,"predict.html")
def logout(request):
    auth.logout(request)
    return redirect('/')


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import AdminDataForm
from django.contrib.auth.decorators import login_required
import json
import os
import csv
from django.contrib import messages
from django.core.serializers import serialize

from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)

def thanks(request):
    data = {
        'description': AdminData.objects.first().thanks
    }

    return render(request, 'thanks.html', data)

def home(request):
    return render(request, 'home.html', {})

def game(request, sessionId):
    if request.method == "POST":
        times = request.POST.get('times', None)
        result = request.POST.get('result', None)
        solutionTime = request.POST.get('solutionTime', None)
        taskNumber = request.POST.get('taskNumber', None)

        if times == None or result == None or solutionTime == None or taskNumber == None:
            msg = "Błędne dane"
        else:
            player = Player.objects.filter(active=True).first()
            if player == None:
                name = "trening"
            else:
                name = player.name
            CardResult.objects.create(name=name, taskNumber=taskNumber, result=result, solutionTime=solutionTime, times=times)
            msg = "OK"

        return HttpResponse(json.dumps({'msg': msg}), content_type="application/json")

    adminData = AdminData.objects.first()

    if sessionId == '1':
        description = adminData.cardSessionTrainingDescription
        timeLimit = adminData.cardSessionTrainingLengthSeconds
    else:
        description = adminData.cardSessionMeasurementDescription
        timeLimit = adminData.cardSessionMeasurementLengthSeconds

    data = {
        'sessionId': sessionId,
        'description': description,
        'timeLimit': timeLimit,
        'redBackgroundTime': adminData.redBackgroundTimeSeconds
    }

    return render(request, 'game.html', data)

def trainingMode(request):
    Player.objects.filter(active=True).update(active=False)
    return game(request, 2)

@login_required(login_url='/admin/login/')
def adminPanel(request):
    if request.method == 'POST':
        form = AdminDataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zmiana zakończona sukcesem.')
            return HttpResponseRedirect('/')
    adminData = [AdminData.objects.get(pk=1)]
    data = '{'+serialize('json', adminData, cls=LazyEncoder)[53:-2]
    data = json.loads(data)
    print(data)
    form = AdminDataForm(initial=data)
    context = {
        'form': form
    }
    return render(request, 'adminPanel.html', context)

def signUp(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
        sex = request.POST.get('sex', None)
        age = request.POST.get('age', None)

        if name == None or sex == None or age == None:
            msg = "Błędne dane"
        elif Player.objects.filter(name=name).exists():
            msg = "Użytkownik " + name + " już istnieje"
        else:
            Player.objects.filter(active=True).update(active=False)
            Player.objects.create(name=name, sex=sex, age=age, active=True)
            msg = "OK"

        return HttpResponse(json.dumps({'msg': msg}), content_type="application/json")

    adminData = AdminData.objects.first()
    if adminData == None:
        initAdminData()
        adminData = AdminData.objects.first()

    data = {
        'welcome': adminData.welcome
    }

    return render(request, 'signUp.html', data)

def GILSession(request, sessionId):
    if request.method == "POST":
        times = request.POST.get('times', None)

        if times == None:
            msg = "Błędne dane"
        else:
            player = Player.objects.get(active=True)
            player.gilSessionTimes = json.loads(times)
            print(times)
            msg = "OK"

        return HttpResponse(json.dumps({'msg': msg}), content_type="application/json")

    adminData = AdminData.objects.first()

    if sessionId == '1':
        description = adminData.gilSessionTrainingDescription
        timeLimit = adminData.gilSessionTrainingLengthSeconds
    else:
        description = adminData.gilSessionMeasurementDescription
        timeLimit = adminData.gilSessionMeasurementLengthSeconds

    data = {
        'sessionId': sessionId,
        'description': description,
        'timeLimit': timeLimit,
        'redBackgroundTime': adminData.redBackgroundTimeSeconds
    }

    return render(request, 'gilSession.html', data)

def initAdminData():
    AdminData.objects.create()

def exportCSV(request):
    filename = 'wyniki.csv'
    with open(filename, 'w') as csvfile:
        rows = []
        writer = csv.writer(csvfile)
        # write your header first
        writer.writerow(['id', 'name', 'task_type', 'result', 'solution_time', 'times'])
        for obj in CardResult.objects.all():
            row = []
            for f in obj._meta.fields:
                row.append(getattr(obj, f.name))
            rows.append(row)
        writer.writerows(rows)
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + filename
        return response

    return HttpResponseRedirect('/')

def exportCSVPlayers(request):
    filename = 'badani.csv'
    with open(filename, 'w') as csvfile:
        rows = []
        writer = csv.writer(csvfile)
        # write your header first
        writer.writerow(['name', 'sex', 'age', 'active'])
        for obj in Player.objects.all():
            row = []
            for f in obj._meta.fields:
                row.append(getattr(obj, f.name))
            rows.append(row)
        writer.writerows(rows)
    with open(filename, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + filename
        return response

    return HttpResponseRedirect('/')
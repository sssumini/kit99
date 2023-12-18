from django.shortcuts import render, redirect
from .models import Stock, MedicalKit
from django.utils import timezone
from django import forms
from django.http import JsonResponse
from django.utils.dateparse import parse_date
import serial
from .models import SearchResult
import requests
from dateutil.relativedelta import relativedelta

# Create your views here.



def searchpage(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        client_id = 'cD9SFepUFYMQgLysXSdO'
        client_secret = 'fucA5wdZAC'
        
        # 변경된 코드 (백과사전 검색)
        url = f'https://openapi.naver.com/v1/search/encyc.json?query={query}'
        # 변경된 코드 (백과사전 검색)
        headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            search_results = data.get('items', [])[:2]
            return render(request, 'main/search/search.html', {'search_results': search_results, 'query': query})
        
    return render(request, 'main/search/search.html')


def stockpage(request):
    if request.method == 'POST':
        try:
            new_stock = Stock()
            new_stock.name = request.POST['name']
            new_stock.quantity = request.POST['quantity']

            new_stock.save()
            return render(request, 'main/main.html')
        except KeyError as e:
            # POST 데이터에서 필요한 키가 누락된 경우
            error_message = f"KeyError: {e}"
            return render(request, 'main/main.html')

    return render(request, 'main/stock/stock.html')



def mainpage(request):
    temperature = 25.5
    humidity = 60.0
    
    context = {
        'temperature': temperature,
        'humidity': humidity,
    }

    return render(request, 'main/main.html', context)

def alarmpage(request):
    temperature = float(request.GET.get('temperature', 90))
    humidity = float(request.GET.get('humidity', 0))

    return render(request, 'main/alarm/alarm.html', {'temperature': temperature, 'humidity': humidity})

def get_sensor_data(request):
    temperature = 25.5
    humidity = 60.0

    #if request.method == 'POST':
    #    temperature = float(request.POST.get('temperature', 0))
    #    humidity = float(request.POST.get('humidity', 0))

    #if temperature > 30.0 or humidity > 80.0:
    #        return render(request, 'alarm.html')
    #return JsonResponse(data)

    data = {
        'temperature': temperature,
        'humidity': humidity,
    }

    return JsonResponse(data)


class MedicalKitForm(forms.ModelForm):
    class Meta:
        model = MedicalKit
        fields = ['purchase_date', 'expiration_date']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }


def deadlinepage(request):
    if request.method == 'POST':
        purchase_date_str = request.POST.get('purchase_date')

        if purchase_date_str:
            purchase_date = parse_date(purchase_date_str)
            if purchase_date:
                medical_kit = MedicalKit.objects.first()
                medical_kit.purchase_date = purchase_date
                medical_kit.expiration_date = purchase_date + relativedelta(days=1095)
                medical_kit.save()

                return redirect('updatepage')

    return render(request, 'main/deadline/deadline.html')

def updatepage(request):
    if request.method == 'POST':
        purchase_date_str = request.POST.get('purchase_date')
        expiration_date_str = request.POST.get('expiration_date')
        expiration_date_str1 = request.POST.get('expiration_date')

        if purchase_date_str:
            purchase_date = parse_date(purchase_date_str)
            if purchase_date:
                medical_kit = MedicalKit.objects.first()
                medical_kit.purchase_date = purchase_date
                medical_kit.expiration_date = purchase_date + relativedelta(days=1095)
                medical_kit.expiration_date1 = purchase_date + relativedelta(days=365)

        if expiration_date_str:
            expiration_date = parse_date(expiration_date_str)
            if expiration_date:
                medical_kit.expiration_date = expiration_date
        
        if expiration_date_str1:
            expiration_date1 = parse_date(expiration_date_str1)
            if expiration_date1:
                medical_kit.expiration_date1 = expiration_date1

        medical_kit.save()

    medical_kit = MedicalKit.objects.first()
    medical_kit.refresh_from_db()  
    return render(request, 'main/deadline/update.html', {'medical_kit': medical_kit})



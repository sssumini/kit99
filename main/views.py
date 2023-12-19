from django.shortcuts import render, redirect
from .models import Stock, MedicalKit
from django.utils import timezone
from django import forms
from django.http import JsonResponse
from django.utils.dateparse import parse_date
import serial
from .models import ArduinoData
from .models import SearchResult
import requests
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404
# Create your views here.


def arduino(request):
    # 시리얼 포트 열기
    ser = serial.Serial('COM4', 9600)  # 포트와 보레이트를 실제 아두이노와 맞게 설정
    # 시리얼 데이터 읽기
    line = ser.readline().decode('utf-8').rstrip()
    # 데이터베이스에 저장
    data_values = line.split(',')
    try:
        temperature = float(data_values[3])
        humidity = float(data_values[4])
    except (ValueError, IndexError):
        temperature = None
        humidity = None

    stock_items = data_values[:3]
    stock_item_names = ["감기약", "면봉", "소화제"]
    for name, quantity_str in zip(stock_item_names, stock_items):
        try:
            quantity = int(quantity_str)
        except ValueError:
            # 정수로 변환할 수 없는 값이면 기본값 0으로 설정하거나 다른 처리 수행
            quantity = 0
        stock_item, created = Stock.objects.get_or_create(name=name)
        stock_item.quantity = quantity
        stock_item.save()
    ArduinoData.objects.create(data=line, temperature=temperature, humidity=humidity)
    # 시리얼 데이터 및 저장 여부를 템플릿으로 전달
    #temperature, humidity = float(data_values[3]), float(data_values[4])
    return render(request, 'main/arduino/arduino.html', {'serial_data': line, 'temperature': temperature, 'humidity': humidity, 'saved_to_database': True})



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
    # Arduino 데이터 확인
    latest_arduino_data = ArduinoData.objects.last()
    quantity_value1, quantity_value2, quantity_value3 = 0, 0, 0

    if latest_arduino_data and ',' in latest_arduino_data.data:
        data_values = latest_arduino_data.data.split(',')
        try:
            # 시리얼 데이터에서 각 약품의 개수 추출
            quantity_value1 = int(data_values[0])
            quantity_value2 = int(data_values[1])
            quantity_value3 = int(data_values[2])
        except ValueError:
            pass

    # "감기약", "소화제"에 대한 Stock 객체 가져오거나 생성
    medical_item1, created1 = Stock.objects.get_or_create(name="감기약")
    medical_item2, created2 = Stock.objects.get_or_create(name="소화제")
    medical_item3, created3 = Stock.objects.get_or_create(name="지사제")

    # 기존에 존재하는 경우 quantity 업데이트
    if not created1:
        medical_item1.quantity = quantity_value1
        medical_item1.save()
    if not created2:
        medical_item2.quantity = quantity_value2
        medical_item2.save()
    if not created3:
        medical_item3.quantity = quantity_value3
        medical_item3.save()

    if request.method == 'POST':
        try:
            # POST 데이터에서 name과 quantity를 받아옴
            name = request.POST.get('name', '')
            quantity_str = request.POST.get('quantity', '')

            # name이 입력되었는지 확인
            if not name:
                raise ValidationError("Name is required")

            # quantity가 입력되었는지 확인
            if quantity_str:
                quantity = int(quantity_str)
            else:
                quantity = 0  # quantity가 입력되지 않은 경우 0으로 설정

            # name에 해당하는 Stock 객체를 가져오거나 없으면 생성
            stock, created = Stock.objects.get_or_create(name=name)
            stock.quantity = quantity
            stock.save()

            return render(request, 'main/main.html')
        except (ValidationError, ValueError) as e:
            # POST 데이터에서 필요한 키가 누락되거나, 숫자로 변환 불가능한 경우
            error_message = f"Error: {e}"
            return render(request, 'main/main.html', {'error_message': error_message})
        except ObjectDoesNotExist as e:
            # Stock 객체가 없는 경우
            error_message = f"ObjectDoesNotExist: {e}"
            return render(request, 'main/main.html', {'error_message': error_message})

    return render(request, 'main/stock/stock.html', {'medical_item1': medical_item1, 'medical_item2': medical_item2, 'medical_item3': medical_item3})


def mainpage(request):
    latest_arduino_data = ArduinoData.objects.last()

    temperature = "값 없음"
    humidity = "값 없음"

    # 최근 데이터가 있다면 온도와 습도 추출
    if latest_arduino_data:
        data_values = latest_arduino_data.data.split(',')
        try:
            temperature = float(data_values[3])
            humidity = float(data_values[4])
        except (IndexError, ValueError):
            # 온도와 습도 값이 없는 경우
            temperature = "값 없음"
            humidity = "값 없음"

    context = {
        'temperature': temperature,
        'humidity': humidity,
    }

    return render(request, 'main/main.html', context)

def alarmpage(request):
    latest_arduino_data = ArduinoData.objects.last()

    temperature = "값 없음"
    humidity = "값 없음"

    # 최근 데이터가 있다면 온도와 습도 추출
    if latest_arduino_data:
        data_values = latest_arduino_data.data.split(',')
        try:
            temperature = float(data_values[3])
            humidity = float(data_values[4])
        except (IndexError, ValueError):
            # 온도와 습도 값이 없는 경우
            temperature = "값 없음"
            humidity = "값 없음"

    context = {
        'temperature': temperature,
        'humidity': humidity,
    }

    return render(request, 'main/alarm/alarm.html', context)


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

from django.utils.dateparse import parse_date
from dateutil.relativedelta import relativedelta

def updatepage(request):
    medical_kit = MedicalKit.objects.first()

    if request.method == 'POST':
        purchase_date_str = request.POST.get('purchase_date')
        expiration_date_str = request.POST.get('expiration_date')
        expiration_date_str1 = request.POST.get('expiration_date1')

        if not medical_kit:
            # medical_kit이 None이면 새로 생성
            medical_kit = MedicalKit.objects.create()

        if purchase_date_str:
            purchase_date = parse_date(purchase_date_str)
            if purchase_date:
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

    return render(request, 'main/deadline/update.html', {'medical_kit': medical_kit})



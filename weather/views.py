from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    appId = "3feea1ea50262d759f165b71230b204b"
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appId

    if(request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm() # очистка поля ввода

    cities = City.objects.all()
    all_cities = []

    # Выводим все города
    for city in cities:
        resp = requests.get(url.format(city.name)).json() # добавляем город в адресную строку и конвертируем в json формат (словарь)
        city_info = {
            'city': city.name,
            'temp' : resp["main"]["temp"],
            'icon': resp["weather"][0]["icon"],
            'humidity' : resp["main"]["humidity"],
        }
        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form} # передаем данные в html

    return render(request, 'weather/index.html', context)

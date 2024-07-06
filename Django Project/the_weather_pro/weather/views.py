from django.shortcuts import render,get_object_or_404,redirect
import requests
from .models import City
from .forms import CityForm

def index(request):
    cities = City.objects.all() 

    url='https://api.openweathermap.org/data/2.5/weather?q={}&appid=0ebb0444cb4bf22d2f05d9874f703d80&units=metric'
    

    
    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save()

    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather) 
    
    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather.html', context) 

def city_delete_view(request,id):
    city=get_object_or_404(City,id=id)
    if request.method=="POST":
        #CONFIRMING TO DELETE
        city.delete()
        return redirect('weather')  # Redirect to the base page after deletion
    context = {"city": city}
    return render(request, "city_delete.html", context)

def city_list_view(request):
    queryset = City.objects.all()
    context = {"city_list": queryset}
    return render(request, "city_list.html", context)

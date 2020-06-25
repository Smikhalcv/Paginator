import csv
import math

from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from app.settings import BUS_STATION_CSV as file_bus_stations


def index(request):
    return redirect(reverse(bus_stations))

def read_csv():
    with open(file_bus_stations) as file:
        reader = csv.DictReader(file, delimiter=',')
        list_path = []
        for line in reader:
            path = {}
            path['Name'] = line['Name']
            path['Street'] = line['Street']
            path['District'] = line['District']
            list_path.append(path)
    return list_path

def bus_stations(request):
    list_path = read_csv()
    count_path_on_page = 20
    count_page = math.ceil(len(list_path)/count_path_on_page)
    paginator_name = Paginator(list_path, count_path_on_page)
    current_page = request.GET.get('page', 1)
    articles = paginator_name.get_page(current_page)
    next_page_url, prev_page_url = None, None
    if articles.has_next():
        next_page_url = articles.next_page_number()
    if articles.has_previous():
        prev_page_url = articles.previous_page_number()
    return render_to_response('index.html', context={
        'bus_stations': articles,
        'current_page': articles.number,
        'count_page': count_page,
        'prev_page_url': '{}?page={}'.format(reverse('bus_stations'), str(prev_page_url)),
        'next_page_url': '{}?page={}'.format(reverse('bus_stations'), str(next_page_url)),
    })
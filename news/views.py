from django.shortcuts import render, redirect
import json
import copy
import random
from datetime import datetime

# Create your views here.
from django.views import View


def get_date(post):
    return post['created']


with open("./news.json", 'r') as f:
    json_data = json.load(f)


def uniqueid():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1


unique_sequence = uniqueid()


def copy_date(data):
    cpy_list = []
    for li in data:
        d2 = copy.deepcopy(li)
        cpy_list.append(d2)
    for li in cpy_list:
        li['created'] = li['created'].split(" ")[0]
    return cpy_list


def welcome_page(request):
    return redirect('/news/')


class MainPageView(View):
    template_name = 'news/index.html'

    def get(self, request):
        sorted_post = sorted(json_data, key=get_date, reverse=True)
        final_post = copy_date(sorted_post)
        context = {
            'news': final_post
        }
        return render(request, self.template_name, context)


class CreateNewsView(View):
    template_name = 'news/create_news.html'

    def get(self, request):
        sorted_post = sorted(json_data, key=get_date, reverse=True)
        final_post = copy_date(sorted_post)
        context = {
            "news": final_post
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        news_dict = {}
        title = request.POST.get('title')
        text = request.POST.get('text')
        link = next(uniqueid())
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Add key, values to dictionary
        for keys in ['created', 'text', 'title', 'link']:
            news_dict[keys] = eval(keys)
        news_dict = news_dict.copy()
        print(news_dict)
        # append news to json data
        json_data.append(news_dict)
        # write json data to disk
        with open('./news.json', 'w') as file:
            json.dump(json_data, file)
        return redirect('/news/')


class SearchNewsView(View):
    template_name = 'news/index.html'

    def get(self, request):
        query = request.GET.get('q')
        # lookup json data and returns all news that contains search
        search_result = [item for item in json_data if item['title'].__contains__(query)]
        context = {
            'search': search_result
        }
        return render(request, template_name=self.template_name, context=context)


class SinglePageView(View):
    template_name = 'news/news.html'

    def get(self, request, link):
        single_news = [li for li in json_data if li['link'] == link]
        context = {
            "news": single_news
        }
        return render(request, self.template_name, context)

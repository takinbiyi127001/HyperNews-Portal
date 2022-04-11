from django.shortcuts import render, redirect
import json
import copy
import random
from datetime import datetime

# Create your views here.
from django.views import View


# filter function used in sorted
def get_date(post):
    return post['created']


# open json file for reading
with open("./news.json", 'r') as f:
    json_data = json.load(f)


# compute unique a id for each link
def uniqueid():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1


unique_sequence = uniqueid()


# extract date from datetime string
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
    """HyperNews Main page - Collect the news articles on one page and display them all to our users."""
    template_name = 'news/index.html'

    def get(self, request):
        sorted_post = sorted(json_data, key=get_date, reverse=True)
        final_post = copy_date(sorted_post)
        context = {
            'news': final_post
        }
        return render(request, self.template_name, context)


class CreateNewsView(View):
    """HyperNews Create news page: a web interface for creating news articles using form
    The link in the storage should be a random number, and it must be unique for every news article.
    Using the current time to populate the created field, and convert it to a string before saving it to JSON."""
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
    """HyperNews Search news- Search functionality to the site
    Add a search form to the main page with one input element with the name q.
    The form should send GET requests to the same /news/ page.
    The format of the result page stays the same but includes only articles
    whose titles match the search term"""
    template_name = 'news/index.html'

    def get(self, request):
        query = request.GET.get('q')
        submit_button = request.GET.get('submit')
        if query is not None:
            # lookup json data and returns all news that contains search
            search_result = [item for item in json_data if item['title'].__contains__(query)]
            sorted_post = sorted(search_result, key=get_date, reverse=True)
            final_post = copy_date(sorted_post)
            context = {
                'submit_button': submit_button,
                'search': final_post
            }
            return render(request, template_name=self.template_name, context=context)
        return redirect('/news/')


class SinglePageView(View):
    """Get single news based on requests"""
    template_name = 'news/news.html'

    def get(self, request, link):
        single_news = [li for li in json_data if li['link'] == link]
        context = {
            "news": single_news
        }
        return render(request, self.template_name, context)

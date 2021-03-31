from django.shortcuts import render, redirect
# from django.conf import settings
import re
from django.views import View
import os
import json
from datetime import datetime





bingo = {'name': 'Harry'}

JSON_PATH = os.path.join(os.getcwd(), 'hypernews/news.json')
def get_sorted_json(json_obj):
    import pandas as pd
    df = pd.DataFrame(json_obj)
    df.index = df['created']
    df_sorted = df.sort_index(ascending=False)
    df_sorted['created_date'] = df_sorted['created'].apply(lambda x: pd.to_datetime(x).date())
    df_sorted['created_date'] = df_sorted['created_date'].apply(lambda x: str(x))
    df_sorted.drop('created',axis=1, inplace=True)
    df_sorted.reset_index(inplace = True)

    new_dc = json.loads(df_sorted.to_json(orient='records'))
    return new_dc

def get_json_item(link=9234732):
    import json

    json_list = json.load(open(JSON_PATH, 'r'))

    for item in json_list:
        if item['link'] == int(link):
            return item
    # if we've exhausted the loop without a return, return empty dict
    return {}


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):

        return render(
            request,
            'index.html',
            context={'bingo': bingo}
        )


class newsMain(View):
    def get(self, request, *args, **kwargs):


        json_list = json.load(open(JSON_PATH, 'r'))
        sorted_json_list = get_sorted_json(json_list)



        return render(request,
                      'news_main.html',
                      context={'sorted_json_list': sorted_json_list})



class NewsView_by_id(View):
    def get(self, request, *args, **kwargs):
        import random

        unique_id = random.randint(10000, 99999)

        pattern = '\d+'
        link_id_string = str(request).split()[2]

        try:
            link_id = int(re.findall(pattern, link_id_string)[0])
        except IndexError:
            link_id = 1

        # insert code here to retrieve the json
        json_response = get_json_item(link_id)

        return render(request,
                      'news_list.html',
                      context={'json_response': json_response, 'link_id': link_id})

class createView(View):
    title = ''
    body = ''
    def get(self, request, *args, **kwargs):
        return render(request,
                      'CreateNews.html',
                      context={"title": self.title,
                               "body": self.body})

    def post(self, request, *args, **kwargs):
        self.title = request.POST.get('title')
        self.body = request.POST.get('text')

        # read the json file first
        json_obj = json.load(open(JSON_PATH))

        new_entry = {'created': datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'),
                     'text': self.body,
                     'title': self.title,
                     'link': len(json_obj)}

        json_obj.append(new_entry)

        # overwrite the file with added new entry
        with open(JSON_PATH, 'w') as w:
            w.write(json.dumps(json_obj))


        return redirect('/news/')

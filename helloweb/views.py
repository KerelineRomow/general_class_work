from django.shortcuts import render
from django.http import HttpResponse
import datetime

from django.views import View
import random


def index(request):
    return HttpResponse("""
            <h1>Hello from my first views function! </h1>
    """)

data = [1,2,3]

def current_datetime(request):
    now = datetime.datetime.now()
    return HttpResponse(f"""
            <h1>Current datetime: {now} </h1>
            <p>Data {data} </p>
    """)

class CurrentDateTime(View):

    def get(self, request):
        now = datetime.datetime.now()
        return HttpResponse(f"""
                    <h1>Current datetime: {now} </h1>
                    <p>Data {data} </p>
            """)


def citata(request):
    rc = [
        "Жизнь — это как езда на велосипеде: если тебе тяжело, значит, ты идешь в гору. А если тебе легко, значит, ты — велосипед.",
        "Если тебе где-то не рады, значит, ты пришел туда, где тебя не ждут.",
        "Лучше один раз упасть, чем сто раз не упасть.",
        "Если ты потерял, значит, у тебя этого нет. А если есть — значит, не терял.",
        "Запомни: если ты один — ты одинок. Но если ты не один, значит, рядом кто-то есть."
    ]

    random_rc = random.choice(rc)

    return HttpResponse(f"<h1>{random_rc}</h1>")




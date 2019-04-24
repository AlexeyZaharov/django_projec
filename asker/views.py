from django.shortcuts import render
from django.http import HttpResponse
from faker import Faker
from django.core.paginator import Paginator
from django.conf import settings as _settings
from asker.models import Answers, Tag, Question, Profile, User

fake = Faker()
questions = Question.objects.all()

def paginator(questions_list, page):
    pager = Paginator(questions_list, _settings.QUESTIONS_CONSTANT)

    try:
        questions_on_page = pager.page(page)
    except:
        questions_on_page = pager.page(1)
    return questions_on_page

def index(request):
    questions_list = paginator(questions, request.GET.get('page'))

    return render(request, 'index.html', {
        'questions': questions_list,
    })


def login(request):
    return render(request, 'login.html', {})


def ask(request):
    return render(request, 'ask.html', {})

def register(request):
    return render(request, 'signup.html', {})


def question(request, id):
    return render(request, 'question.html', {'question': questions.get(id=id)})


def settings(request):
    return render(request, 'settings.html', {})


def tag(request, tag):
    tag_questions = Question.objects.filter(tags__title=tag)
    questions_list = paginator(tag_questions, request.GET.get('page'))

    return render(request, 'tag.html', {
        'questions': questions_list,
        'tag': tag,
    })


def hot(request):
    hot_questions = Question.objects.best()
    questions_list = paginator(hot_questions, request.GET.get('page'))

    return render(request, 'hot.html', {
        'questions': questions_list,
    })


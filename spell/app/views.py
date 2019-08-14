# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import randint
from django.shortcuts import render
from .models import User, Test, WordList
import re

# Create your views here.

def read():
    import urllib

    link = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt"
    f = urllib.urlopen(link)
    myfile = str(f.read())
    for line in myfile.splitlines():
        word = WordList.objects.create(word=line,length=line.__len__())
        word.save()


def example(query):
    import urllib

    link = "https://skell.sketchengine.co.uk/run.cgi/concordance?lpos=&query=" + query
    f = urllib.urlopen(link)
    html = str(f.read())
    res = ''
    for line in html.splitlines():
        if line.lstrip().startswith('<span class="lc">'):
            res = res + \
                re.sub('\</span>$', '', re.sub('^<span class="lc">',
                                               '', line.lstrip().rstrip()))
        if line.lstrip().startswith('<span class="kw">'):
            res = res + \
                re.sub('\</span>$', '', re.sub('^<span class="kw">',
                                               '', line.lstrip().rstrip()))
        if line.lstrip().startswith('<span class="rc">'):
            res = res + \
                re.sub('\</span>$', '', re.sub('^<span class="rc">',
                                               '', line.lstrip().rstrip()))
            return res


def get_user(request):
    try:
        user = User.objects.get(email=request.session['email'])
    except User.DoesNotExist:
        user = None
    return user


def get_word(test):
    word_list = WordList.objects.all().filter(id__gte=test.min_rank, id__lte=test.max_rank,
                                              length__gte=test.min_len, length__lte=test.max_len)
    # word_list = WordList.objects.all().filter(id__lte = 4)
    #read()
    size = len(word_list)
    ind = randint(0, size-1)
    return word_list[ind].word, word_list[ind].id


def index(request):
    if request.session.has_key('email'):
        user = get_user(request)
        if user is not None:
            context = {'start': user.start}
            if user.start == 1:
                test = Test.objects.get(id=user.test_id)
                context['correct'] = test.correct
                context['wrong'] = test.wrong
                total = test.correct + test.wrong
                if total != 0:
                    context['percent'] = test.correct * 100 / total
                else:
                    context['percent'] = 0
                word, rank = get_word(test)
                context['word'] = word
                context['rank'] = rank
                context['example'] = "test"#example(context['word'])
                # for word in WordList.objects.all().values_list('word'):
                #     try:
                #         print word[0] + " : " + example(word[0])
                #     except:
                #         print "error"

            return render(request, 'app/index.html', context)

    else:
        return login(request)


def login(request):
    if request.session.has_key('email'):
        return index(request)
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('pass')
            try:
                user = User.objects.get(email=email, password=password)
            except User.DoesNotExist:
                user = None
            if user is not None:
                request.session['name'] = user.name
                request.session['email'] = email
                # read()
                return index(request)
    return render(request, 'app/login.html', {})


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        cpass = request.POST.get('cpass')
        if password != cpass:
            return login(request)
        user = User.objects.create(name=name, email=email, password=password)
        user.save()
        request.session['name'] = name
        request.session['email'] = email
        return index(request)
    else:
        return login(request)


def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return login(request)


def start(request):
    if request.method == 'POST':
        user = get_user(request)
        if user is None:
            return index(request)
        min_len = request.POST.get('min_len')
        max_len = request.POST.get('max_len')
        min_rank = request.POST.get('min_rank')
        max_rank = request.POST.get('max_rank')
        if (min_len > max_len) | (min_rank > max_rank):
            return index(request)
        test = Test.objects.create(
            uid=user.id, min_len=min_len, max_len=max_len, min_rank=min_rank, max_rank=max_rank)
        test.save()
        user.start = 1
        user.test_id = test.id
        user.save()
    return index(request)


def stop(request):
    if request.session.has_key('email'):
        if request.method == 'POST':
            user = get_user(request)
            if user is None:
                return index(request)
            user.start = 0
            user.save()
        return index(request)
    else:
        return login(request)


def check(request):
    if request.session.has_key('email'):
        if request.method == 'POST':
            user = get_user(request)
            if user is None:
                return index(request)
            word = request.POST.get('word')
            ans = request.POST.get('ans')
            test = Test.objects.get(id=user.test_id)
            request.session['word'] = word
            if word.lower() != ans.lower():
                request.session['res'] = 'wrong'
                test.wrong = test.wrong + 1
            else:
                request.session['res'] = 'correct'
                test.correct = test.correct + 1
            test.save()

        return index(request)
    else:
        return login(request)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import logging
import random

from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render

from .apps import EN_HI_DICT
from .models import Result, Test, User, WordInfo, WordList

# Create your views here.
logging.basicConfig(level=logging.DEBUG)

def get_hindi(word):
    word_s = '"%s"' % word
    word_info = EN_HI_DICT.get(word_s)
    if word_info:
        return word_info
    elif word.endswith('s'):
        return get_hindi(word[:len(word) - 1])


def get_user(request):
    try:
        user = User.objects.get(email=request.session['email'])
    except User.DoesNotExist:
        user = None
    return user


def get_word(test, request):
    word_list = Result.objects.all().filter(test_id=test.id).order_by("rank")
    current_word_idx = test.current_word_idx
    total_words = test.total_words

    if current_word_idx >= total_words:
        if word_list:
            test.completed = 1
        return (None, None)
    request.session['progress_percent'] = (current_word_idx * 100 //
                                           total_words)

    if word_list:
        word_obj = word_list[current_word_idx]
        return word_obj.word, word_obj.rank
    return (None, None)


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
                    context['correct_percent'] = test.correct * 100 // total
                else:
                    context['correct_percent'] = 0
                word, rank = get_word(test, request)
                if test.completed:
                    logging.info("This test is completed.")
                    test.save()
                    return stop(request)
                if word is None:
                    logging.error("could not find any word for this test.")
                    return stop(request)
                context['word'] = word
                context['rank'] = rank
                context['hindi'] = get_hindi(word)
                context['current_word_idx'] = test.current_word_idx
                context['total_words'] = test.total_words
                context[
                    'progress_percent'] = test.current_word_idx * 100 // test.total_words
                previous_words_list = []
                words_list = Result.objects.all().filter(
                    test_id=test.id).order_by("rank")
                for word in words_list:
                    if word.answer != '-1' and word.word != word.answer:
                        previous_words_list.append({
                            'word': word.word,
                            'answer': word.answer,
                            'result' : 'correct' if word.word == word.answer else 'wrong'
                        })
                context['previous_words_list'] = previous_words_list


            else:
                test_list = Test.objects.all().filter(uid=user.id).order_by("-id")
                test_results = []
                for test in test_list:
                    test_results.append({
                        "id" : test.id,
                        "min_len": test.min_len,
                        "max_len": test.max_len,
                        "min_rank": test.min_rank,
                        "max_rank": test.max_rank,
                        "correct": test.correct,
                        "wrong": test.wrong,
                        "total": test.correct + test.wrong,
                        "percent": (test.correct *100) // (test.correct + test.wrong) if (test.correct + test.wrong) != 0 else 0,
                        "completed": test.completed,
                        "current_word_idx": test.current_word_idx,
                        "total_words": test.total_words
                    })
                context['test_results'] = test_results

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
                #read()
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
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            # user. is already registered
            return render(request, 'app/login.html', {})
        user = User.objects.create(name=name, email=email, password=password)
        user.save()
        request.session['name'] = name
        request.session['email'] = email
        return index(request)
    else:
        return login(request)


def logout(request):
    request.session.clear()
    return login(request)


def filter_word_list(uid, word_list):
    new_word_list = []
    for word in word_list:
        try:
            word_info = WordInfo.objects.get(word=word.word, uid=uid)
            score = word_info.correct - word_info.wrong * 2.5
        except WordInfo.DoesNotExist:
            score = 0
        if score <= 0:
            new_word_list.append(word)
        else:
            random_no = random.randint(1, 100)
            if random_no < 80:
                new_word_list.append(word)
    return new_word_list


def start(request):
    if request.method == 'POST':
        user = get_user(request)
        if user is None:
            logging.error("user is None.")
            return index(request)
        min_len = int(request.POST.get('min_len'))
        max_len = int(request.POST.get('max_len'))
        min_rank = int(request.POST.get('min_rank'))
        max_rank = int(request.POST.get('max_rank'))
        if (min_len > max_len) or (min_rank >= max_rank):
            logging.error("test condition failed.")
            return index(request)
        word_list = WordList.objects.all().filter(id__gte=min_rank,
                                                id__lte=max_rank,
                                                length__gte=min_len,
                                                length__lte=max_len)
        if word_list:

            test = Test.objects.create(uid=user.id,
                                       min_len=min_len,
                                       max_len=max_len,
                                       min_rank=min_rank,
                                       max_rank=max_rank,
                                       total_words=len(word_list))

            total_selected_words = 0
            word_list = filter_word_list(user.id, word_list)
            for word in word_list:
                result = Result.objects.create(test_id=test.id, word=word.word.lower(), answer='-1', rank=word.id)
                total_selected_words = total_selected_words + 1
                result.save()

            test.total_words = total_selected_words
            test.save()
            user.start = 1
            user.test_id = test.id
            user.save()
        else:
            logging.error("could not find any word for this test.")
    return index(request)


def stop(request):
    if request.session.has_key('email'):
        if request.method == 'POST':
            user = get_user(request)
            if user is None:
                return index(request)

            if user.start:
                user.start = 0
                user.save()
            else:
                logging.info("user is not attempting any test.")
        return index(request)
    else:
        return login(request)


def check(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.session.has_key('email'):
        if request.method == 'POST':
            user = get_user(request)
            if user is None:
                return index(request)
            if user.start == 0:
                return index(request)
            word = request.POST.get('word')
            ans = request.POST.get('ans')
            test = Test.objects.get(id=user.test_id)
            try:
                word_info = WordInfo.objects.get(word=word, uid=user.id)
            except WordInfo.DoesNotExist:
                word_info = None

            if word_info is None:
                word_info = WordInfo.objects.create(word=word, uid=user.id)
            request.session['word'] = word
            result = Result.objects.get(test_id=test.id, word=word.lower())
            result.answer = ans.lower()
            if word.lower() != ans.lower():
                request.session['res'] = 'wrong'
                test.wrong = test.wrong + 1
                word_info.wrong = word_info.wrong + 1
            else:
                request.session['res'] = 'correct'
                test.correct = test.correct + 1
                word_info.correct = word_info.correct + 1

            if not test.completed:
                test.current_word_idx = test.current_word_idx + 1

            result.save()
            test.save()
            word_info.save()

        return index(request)
    else:
        return login(request)

def word_info(request):
    context = {}
    if request.session.has_key('email'):
        user = get_user(request)
        if user is None:
            return index(request)
        context = {}
        word_info_result_set = WordInfo.objects.all().filter(uid=user.id)
        word_info_list = []
        for word in word_info_result_set:
            word_info_list.append({
                'id': word.id,
                'word': word.word,
                'correct': word.correct,
                'wrong': word.wrong,
                'score': word.correct - word.wrong*2.5
            })
        word_info_list = filter(
            lambda x: x['score'] <= 0,
            sorted(word_info_list, key=lambda i: i['score']))
        context['improvement_list'] = word_info_list

        return render(request, 'app/word_info.html', context)
    return index(request)


def traning(request):
    pass


def resume_test(request):
    """
    resume a paused test
    """
    if request.session.has_key('email'):
        if request.method == 'POST':
            user = get_user(request)
            if user is None:
                return index(request)
            if user.start == 0:
                test_id = request.POST.get('test-id')
                if test_id is None:
                    logging.error("test-id is None.")
                    return index(request)
                test = Test.objects.get(id=test_id)
                if not test.completed:
                    user.start = 1
                    user.test_id = test_id
                    user.save()
                else:
                    logging.error('test is already completed.')
            else:
                logging.info("user is already attempting a test. Please stop running test before resuming another test.")
        return index(request)
    else:
        return login(request)

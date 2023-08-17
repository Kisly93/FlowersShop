from django.shortcuts import render
from .models import Bouquet, BouquetItem, Flower


def index(request):
    return render(request, 'index.html', {})


def catalog(request):
    bouquets = Bouquet.objects.all()
    context = {
        'bouquets': bouquets,
    }
    return render(request, "catalog.html", context=context)


def card(request):
    # print(request.GET)
    # print(request.content_params)
    return render(request, 'card.html', {})


def consultation(request):
    return render(request, 'consultation.html', {})


def order(request):
    return render(request, 'order.html', {})


def order_step(request):
    return render(request, 'order-step.html', {})


def quiz(request):
    return render(request, 'quiz.html', {})


def quiz_step(request):
    return render(request, 'quiz-step.html', {})


def result(request):
    return render(request, 'result.html', {})

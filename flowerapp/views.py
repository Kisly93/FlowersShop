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
    bouquet = Bouquet.objects.filter(pk=int(request.POST.get("select_bouquet"))).first()
    bouquet_items = BouquetItem.objects.filter(bouquet=bouquet)
    # здесь конструкция bouquet_items = bouquet.bouquet_items почему то не передается в шаблон как QuerySet
    context = {
        'bouquet': bouquet,
        'bouquet_items': bouquet_items,
    }
    return render(request, 'card.html', context=context)


def consultation(request):
    return render(request, 'consultation.html', {})


def order(request):
    print(request.POST.get('make_order'))
    return render(request, 'order.html', {})


def order_step(request):
    return render(request, 'order-step.html', {})


def quiz(request):
    return render(request, 'quiz.html', {})


def quiz_step(request):
    return render(request, 'quiz-step.html', {})


def result(request):
    return render(request, 'result.html', {})

from django.shortcuts import render
from phonenumber_field.phonenumber import PhoneNumber
from django.http import HttpResponse
from .models import Bouquet, BouquetItem, Order, Client


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
    context = {
        'bouquet_pk': request.POST.get('make_order'),
    }
    return render(request, 'order.html', context=context)


def order_step(request):
    serialized_phone = PhoneNumber.from_string(request.POST.get('tel'), region='RU').as_e164
    client, client_created = Client.objects.get_or_create(
        phone_number=serialized_phone,
        defaults={'name': request.POST.get('fname')},
    )

    bouquet = Bouquet.objects.get(pk=request.POST.get('bouquet_pk'))
    order = Order(
        client=client,
        address=request.POST.get('adress'),
        delivery_time=request.POST.get('orderTime'),
        cost=bouquet.price,
    )
    order.save()
    order.bouquet.add(bouquet)
    return render(request, 'order-step.html', {})


def quiz(request):
    return render(request, 'quiz.html', {})


def quiz_step(request):
    return render(request, 'quiz-step.html', {})


def result(request):
    return render(request, 'result.html', {})

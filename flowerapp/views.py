import random

from django.shortcuts import render
from phonenumber_field.phonenumber import PhoneNumber
from django.http import HttpResponse
from .models import Bouquet, BouquetItem, Order, Client
import stripe
from django.shortcuts import render
from django.http import JsonResponse
from environs import Env


env = Env()
stripe.api_key = env('STRIPE_API_KEY')


def process_payment(request):
    if request.method == 'POST':
        email = request.POST.get('mail', '')
        payment_success = False
        payment_failed = False

        try:
            order_cost = request.session.get('order_cost', 0)
            charge = stripe.Charge.create(
                amount=order_cost * 100,
                currency="usd",
                source="tok_visa",  # Используем тестовый токен
                description="Оплата заказа",
                receipt_email=email,
            )
            payment_success = True
        except stripe.error.CardError as e:
            payment_failed = True
        except stripe.error.StripeError as e:
            payment_failed = True

        if payment_success:
            order = Order.objects.get(pk=request.session.get('order_pk', 0))
            order.payed = True
            order.save()

        context = {
            'payment_success': payment_success,
            'payment_failed': payment_failed,
            'order_cost': order_cost,
        }
        return render(request, 'order-step.html', context)


def index(request):
    selected_bouquets = list(Bouquet.objects.all())
    random_selected_bouquets = random.sample(selected_bouquets, k=3)
    return render(request, 'index.html', {'bouquets': random_selected_bouquets})


def catalog(request):
    bouquets = Bouquet.objects.all()
    return render(request, "catalog.html", {'bouquets': bouquets})


def card(request):
    bouquet = Bouquet.objects.get(pk=int(request.POST.get("select_bouquet")))
    bouquet_items = BouquetItem.objects.filter(bouquet=bouquet)
    # здесь конструкция bouquet_items = bouquet.bouquet_items почему то не передается в шаблон как QuerySet
    return render(request, 'card.html', {'bouquet': bouquet, 'bouquet_items': bouquet_items})


def consultation(request):
    return render(request, 'consultation.html', {})


def order(request):
    return render(request, 'order.html', {'bouquet_pk': request.POST.get('make_order')})


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
    request.session['order_pk'] = order.pk
    request.session['order_cost'] = order.cost
    return render(request, 'order-step.html', {'order_cost': order.cost})


def quiz(request):
    return render(request, 'quiz.html', {})


def quiz_step(request):
    request.session['category'] = request.POST.get('category')
    return render(request, 'quiz-step.html', {})


def result(request):
    if request.POST.get('price'):
        min_price, max_price = request.POST.get('price').split('-')
    else:
        min_price, max_price = 0, 999999

    selected_bouquets = Bouquet.objects.filter(
            category=request.session['category'],
    )
    if selected_bouquets:
        try:
            selected_bouquets = list(Bouquet.objects.filter(
                category=request.session['category'],
                price__range=(min_price, max_price),
            ))
            random_selected_bouquet = random.choice(selected_bouquets)
        except IndexError:
            selected_bouquets = list(Bouquet.objects.filter(
                category=request.session['category'],
            ))
            random_selected_bouquet = random.choice(selected_bouquets)
    else:
        try:
            selected_bouquets = list(Bouquet.objects.filter(
                price__range=(min_price, max_price),
            ))
            random_selected_bouquet = random.choice(selected_bouquets)
        except IndexError:
            selected_bouquets = list(Bouquet.objects.all())
            random_selected_bouquet = random.choice(selected_bouquets)

    bouquet_items = BouquetItem.objects.filter(bouquet=random_selected_bouquet)
    return render(request, 'result.html', {'bouquet': random_selected_bouquet, 'bouquet_items': bouquet_items})

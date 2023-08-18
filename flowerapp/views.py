import random

from django.shortcuts import render
from phonenumber_field.phonenumber import PhoneNumber
from django.http import HttpResponse
from .models import Bouquet, BouquetItem, Order, Client
import stripe
from django.shortcuts import render
from django.http import JsonResponse
stripe.api_key = "sk_test_51NgQ5TE6lrzSQB6jSOLNM5nMlQWgKbZmsBAx8wvY6aJynJZdibHWvYwMdwDfpClWAzmFAMNfSgU7nNLQGNhPAzxk00OwkJ74La"
def process_payment(request):
    if request.method == 'POST':
        email = request.POST.get('mail', '')
        payment_success = False
        payment_failed = False

        try:
            bouquet_amount = request.session.get('bouquet_amount', 0)
            charge = stripe.Charge.create(
                amount=bouquet_amount * 100,
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

        context = {
            'payment_success': payment_success,
            'payment_failed': payment_failed,
            'bouquet_amount': bouquet_amount,
        }
        return render(request, 'order-step.html', context)

def index(request):
    return render(request, 'index.html', {})


def catalog(request):
    bouquets = Bouquet.objects.all()
    context = {
        'bouquets': bouquets,
    }
    return render(request, "catalog.html", context=context)


def card(request):
    bouquet = Bouquet.objects.get(pk=int(request.POST.get("select_bouquet")))
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
    context = {
        'bouquet_amount': order.cost,
    }
    request.session['bouquet_amount'] = order.cost
    return render(request, 'order-step.html', context)



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

    context = {
        'bouquet': random_selected_bouquet,
        'bouquet_items': bouquet_items,
    }

    return render(request, 'result.html', context=context)

import random
import telegram
import phonenumbers
import stripe

from django.http import HttpResponse
from django.shortcuts import render
from .models import Bouquet, BouquetItem, Order, Client

from phonenumber_field.phonenumber import PhoneNumber
from environs import Env


env = Env()
stripe.api_key = env('STRIPE_API_KEY')
telegram_owner_id = env('TELEGRAM_OWNER_ID')
bot = telegram.Bot(token=env('TELEGRAM_TOKEN'))


def process_payment(request):
    if request.method == 'POST':
        email = request.POST.get('mail', '')
        payment_success = False
        payment_failed = False
        order_cost = request.session.get('order_cost', 0)
        try:
            stripe.Charge.create(
                amount=order_cost * 100,
                currency="usd",
                source="tok_visa",  # Используем тестовый токен
                description="Оплата заказа",
                receipt_email=email,
            )
            payment_success = True
        except stripe.error.CardError:
            payment_failed = True
        except stripe.error.StripeError:
            payment_failed = True

        if payment_success:
            new_order = Order.objects.get(pk=request.session.get('order_pk', 0))
            new_order.payed = True
            new_order.save()

        context = {
            'payment_success': payment_success,
            'payment_failed': payment_failed,
            'order_cost': order_cost,
        }
        return render(request, 'order-step.html', context)


def index(request):
    request.session.clear()
    selected_bouquets = list(Bouquet.objects.all())
    random_selected_bouquets = random.sample(selected_bouquets, k=3)
    return render(request, 'index.html', {'bouquets': random_selected_bouquets})


def catalog(request):
    request.session.clear()
    bouquets = Bouquet.objects.all()
    return render(request, "catalog.html", {'bouquets': bouquets})


def card(request):
    bouquet = Bouquet.objects.get(pk=int(request.POST.get("select_bouquet")))
    request.session['bouquet_pk'] = bouquet.pk
    request.session['bouquet_name'] = bouquet.name
    bouquet_items = BouquetItem.objects.filter(bouquet=bouquet)
    return render(request, 'card.html', {'bouquet': bouquet, 'bouquet_items': bouquet_items})


def permited(request):
    return render(request, 'permited.html', {})


def contacts(request):
    return render(request, 'contacts_page.html', {})


def consultation(request):
    return render(request, 'consultation.html', {})


def consultation_ok(request):
    check_result, serialized_phone = check_phone(request)
    if not check_result:
        return render(request, 'consultation.html',
            {
                'phone_not_valid': serialized_phone,
                'fname': request.POST.get('fname'),
                'tel': request.POST.get('tel'),
            }
        )

    client_name = request.POST.get('fname')
    phone_number = "".join(request.POST.get('tel').split())
    message_to_owner = f'Клинет {client_name} просит перезвонить для консультации. \nТелефон: {phone_number}.'
    if request.session.get('bouquet_pk'):
        message_to_owner += f'\nВероятно по поводу букета "{request.session.get("bouquet_name")}"'
    try:
        bot.send_message(telegram_owner_id, message_to_owner)
    except telegram.error.NetworkError as error:
        return HttpResponse(f'Ошибка сайта. Повторите попытку позже. \n{error}')
    return render(request, 'consultation_ok.html', {'client_name': client_name, 'phone_number': phone_number})


def order(request):
    return render(request, 'order.html', {'bouquet_pk': request.session.get('bouquet_pk', 0)})


def check_phone(request):
    serialized_phone = PhoneNumber.from_string(request.POST.get('tel'), region='RU').as_e164
    if not phonenumbers.is_valid_number(phonenumbers.parse(serialized_phone)):
        return False, f'Номер телефона {serialized_phone} не является корректным!'
    return True, serialized_phone


def order_step(request):
    check_result, serialized_phone = check_phone(request)
    if not check_result:
        return render(request, 'order.html',
            {
                'phone_not_valid': serialized_phone,
                'fname': request.POST.get('fname'),
                'tel': request.POST.get('tel'),
                'adress': request.POST.get('adress'),
            }
        )

    client, client_created = Client.objects.get_or_create(
        phone_number=serialized_phone,
        defaults={'name': request.POST.get('fname')},
    )

    bouquet = Bouquet.objects.get(pk=request.session.get('bouquet_pk', 0))
    new_order = Order(
        client=client,
        address=request.POST.get('adress'),
        delivery_time=request.POST.get('orderTime'),
        cost=bouquet.price,
    )
    new_order.save()
    new_order.bouquet.add(bouquet)

    message_to_owner = f'''
        В магазине сделан заказ:
        букет: {bouquet.name},
        сумма: {new_order.cost},
        адрес доставки: {new_order.address},
        время доставки: {Order.DeliveryTime(new_order.delivery_time).label},
        клиент: {client.name},
        телефон: {client.phone_number}        
    '''
    try:
        bot.send_message(telegram_owner_id, message_to_owner)
    except telegram.error.NetworkError as error:
        return HttpResponse(f'Ошибка сайта. Повторите попытку позже. \n{error}')

    request.session['order_pk'] = new_order.pk
    request.session['order_cost'] = new_order.cost
    return render(request, 'order-step.html', {'order_cost': new_order.cost})


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

    request.session['bouquet_pk'] = random_selected_bouquet.pk
    request.session['bouquet_name'] = random_selected_bouquet.name
    bouquet_items = BouquetItem.objects.filter(bouquet=random_selected_bouquet)
    return render(request, 'result.html', {'bouquet': random_selected_bouquet, 'bouquet_items': bouquet_items})

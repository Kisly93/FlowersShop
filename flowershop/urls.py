
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from flowerapp import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('card/', views.card, name='card'),
    path('consultation/', views.consultation, name='consultation'),
    path('consultation_ok/', views.consultation_ok, name='consultation_ok'),
    path('order/', views.order, name='order'),
    path('order-step/', views.order_step, name='order-step'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz-step/', views.quiz_step, name='quiz-step'),
    path('result/', views.result, name='result'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('permited/', views.permited, name='permited'),
    path('contacts/', views.contacts, name='contacts'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

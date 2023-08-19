from django.contrib import admin
from django.utils.html import format_html
from django_object_actions import DjangoObjectActions, action
from .models import Bouquet, Flower, BouquetItem, Packaging, Ribbon, Client, Order
from rangefilter.filters import NumericRangeFilterBuilder
from .functions import update_price


class BouquetItemInline(admin.TabularInline):
    model = BouquetItem
    extra = 0


@admin.register(Bouquet)
class BouquetAdmin(DjangoObjectActions, admin.ModelAdmin):

    list_display = (
        'name',
        'flowers',
        'packaging',
        'ribbon',
        'category',
        'height',
        'width',
        'price',
        'dont_update_price',
        'admin_image',
    )

    list_filter = [
        'category',
        'dont_update_price',
        ('height', NumericRangeFilterBuilder()),
        ('width', NumericRangeFilterBuilder()),
    ]

    search_fields = [
        'category',
        'name',
    ]

    @action(label='Обновить цены букетов', description='Обновить цены по всем букетам, у которых не стоит '
                                                       'запрет на обновление')
    def update_all_prices(self, request, obj):
        bouquets = Bouquet.objects.all()
        for bouquet in bouquets:
            update_price(bouquet)

    changelist_actions = ('update_all_prices', )

    def admin_image(self, obj):
        if obj.image:
            return format_html(
                f'''<a href="{obj.image.url}" target="_blank">
                  <img src="{obj.image.url}" alt="{obj.image}" 
                    width="50" height="50" style="object-fit: cover;"/></a>
                ''')
    admin_image.allow_tags = True

    def save_model(self, request, obj, form, change):
        update_price(obj)
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        try:
            bouquet = instances[0].bouquet
            for instance in instances:
                instance.save()
            formset.save_m2m()
            update_price(bouquet)
        except IndexError:
            pass

    def flowers(self, row):
        return ', '.join([f'{bouquet_item.flower.name} {bouquet_item.quantity}шт'
                          for bouquet_item in row.bouquet_items.select_related('flower').all()])
    flowers.short_description = 'Цветы'

    inlines = [
        BouquetItemInline
    ]


class BouquetInline(admin.TabularInline):
    model = Bouquet
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'bouquets',
        'cost',
        'address',
        'delivery_time',
        'status',
        'payed',
    )

    def bouquets(self, row):
        return ', '.join([bouquet.name for bouquet in row.bouquet.all()])
    bouquets.short_description = 'Букеты'

    search_fields = [
        'address',
    ]

    list_filter = [
        'status',
    ]


admin.site.register(Flower)
admin.site.register(Packaging)
admin.site.register(Ribbon)
admin.site.register(Client)

admin.site.site_header = 'Панель управляющего магазином'
admin.site.site_title = '"FlowersShop"'
admin.site.index_title = 'Доступные разделы:'

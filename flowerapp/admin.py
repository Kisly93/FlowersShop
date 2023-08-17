from django.contrib import admin
from django.utils.html import format_html
from django_object_actions import DjangoObjectActions, action
from .models import Bouquet, Flower, BouquetItem, Packaging, Ribbon, Client, Order


class BouquetItemInline(admin.TabularInline):
    model = BouquetItem
    extra = 0


@admin.register(Bouquet)
class BouquetAdmin(DjangoObjectActions, admin.ModelAdmin):

    @action(label='Обновить цены букетов', description='Обновить цены по всем букетам, у которых не стоит '
                                                       'запрет на обновление')
    def update_price(self, request, obj):
        bouquets = Bouquet.objects.all()
        for bouquet in bouquets:
            if not bouquet.dont_update_price:
                bouquet_items = bouquet.bouquet_items
                bouquet_price = 0
                for bouquet_item in bouquet_items.values():
                    bouquet_price += Flower.objects.filter(pk=bouquet_item["flower_id"])[0].price * bouquet_item["quantity"]
                bouquet.price = bouquet_price
                bouquet.save()

    changelist_actions = ('update_price', )

    def admin_image(self, obj):
        if obj.image:
            return format_html(
                f'''<a href="{obj.image.url}" target="_blank">
                  <img src="{obj.image.url}" alt="{obj.image}" 
                    width="50" height="50" style="object-fit: cover;"/></a>
                ''')

    admin_image.allow_tags = True

    search_fields = [
        'category',
    ]

    list_display = (
        'name',
        'flowers',
        'packaging',
        'ribbon',
        'category',
        'price',
        'dont_update_price',
        'admin_image',
    )

    list_filter = [
        'category',
        'dont_update_price',
    ]

    def flowers(self, row):
        return ', '.join([bouquet_item.flower.name for bouquet_item in row.bouquet_items.select_related('flower').all()])
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

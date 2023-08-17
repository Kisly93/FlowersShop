from django.contrib import admin
from django.utils.html import format_html

from .models import Bouquet, Flower, BouquetItem, Packaging, Ribbon, Client, Order


class BouquetItemInline(admin.TabularInline):
    model = BouquetItem
    extra = 0


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):

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
        'admin_image',
    )

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

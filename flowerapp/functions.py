from .models import Flower


def update_price(bouquet):
    if not bouquet.dont_update_price:
        bouquet_items = bouquet.bouquet_items
        bouquet_price = 0
        for bouquet_item in bouquet_items.values():
            bouquet_price += Flower.objects.filter(pk=bouquet_item["flower_id"])[0].price * bouquet_item["quantity"]
        try:
            bouquet_price += bouquet.packaging.price
        except AttributeError:
            pass
        try:
            bouquet_price += bouquet.ribbon.price
        except AttributeError:
            pass
        bouquet.price = bouquet_price
        bouquet.save()

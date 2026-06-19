
from .cart import Cart
from shop.models import Category
from shop.translations import TRANSLATIONS

def cart(request):
    lang = request.session.get('language', 'fa')
    return {
        'cart': Cart(request),
        'nav_categories': Category.objects.all(),
        'lang': lang,
        'T': TRANSLATIONS.get(lang, TRANSLATIONS['en']),
    }
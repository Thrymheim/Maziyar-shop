from django import template
from shop.translations import TRANSLATIONS

register = template.Library()

@register.simple_tag
def trans(key, lang='fa'):
    return TRANSLATIONS.get(lang, TRANSLATIONS['fa']).get(key, key)

@register.simple_tag
def trans_attr(key, lang='fa'):
    return TRANSLATIONS.get(lang, TRANSLATIONS['fa']).get(key, key)

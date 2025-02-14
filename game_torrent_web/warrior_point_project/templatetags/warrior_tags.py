from django import template
from warrior_point.models import Category

register = template.Library()

@register.simple_tag()  # Декоретер позволит вызывать функцию в любом html
def get_categories():
    return Category.objects.all()

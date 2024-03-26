from django import template

register = template.Library()

@register.filter(name="set_value")
def set_value(value):
    return '{:,}'.format(value)
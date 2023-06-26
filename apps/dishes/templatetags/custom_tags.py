from django import template

register = template.Library()

@register.filter
def round_thousands(number):
    rounded_number = round(int(number), -3)
    return rounded_number

@register.filter
def multiply(value, arg):
    return value * arg
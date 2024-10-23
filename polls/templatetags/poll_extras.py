from django import template

register = template.Library()

@register.filter(name='three_digits_currency')
def three_digits_currency(value):
    try:
        value = value if isinstance(value, int) else int(value)
    except:
        return None
    return  'تومان ' + '{:,}'.format(value)
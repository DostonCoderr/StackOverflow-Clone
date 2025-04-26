from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """Matnni berilgan ajratuvchi bo'yicha bo'lish."""
    if value:
        return value.split(delimiter)
    return []

@register.filter
def strip(value):
    """Matndan bo'sh joylarni olib tashlash."""
    if value:
        return value.strip()
    return value
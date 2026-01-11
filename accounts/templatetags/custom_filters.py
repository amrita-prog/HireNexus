from django import template

register = template.Library()

@register.filter
def get_index(lst, index):
    """Get item from list by index"""
    try:
        return lst[index]
    except (IndexError, TypeError, AttributeError):
        return ''

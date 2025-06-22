from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """
    Subtracts the arg from the value.
    """
    return value - arg

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using the key."""
    return dictionary.get(key) 
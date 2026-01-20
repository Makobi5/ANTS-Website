from django import template
from academics.models import Program

register = template.Library()

@register.simple_tag
def get_featured_programs():
    # Returns all programs where the checkbox is ticked
    return Program.objects.filter(is_featured_in_menu=True).order_by('title')
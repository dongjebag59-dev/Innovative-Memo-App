import re
from django import template
from django.utils.html import conditional_escape, mark_safe

register = template.Library()


@register.filter
def split(value, sep=","):
    if not value:
        return []
    return [v.strip() for v in value.split(sep)]


@register.filter(needs_autoescape=True)
def highlight(text, query, autoescape=True):
    if not query or not text:
        return conditional_escape(text) if autoescape else text
    escaped = conditional_escape(str(text))
    for word in str(query).split():
        if not word:
            continue
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        escaped = pattern.sub(
            lambda m: f'<mark>{conditional_escape(m.group())}</mark>',
            escaped,
        )
    return mark_safe(escaped)

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user==context['user']:
        return "Vous avez"
    return f"{user.username.capitalize()} a"

@register.simple_tag(takes_context=True)
def get_poster_display_subject(context, user):
    if user==context['user']:
        return "Vous"
    return f"{user.username.capitalize()}"

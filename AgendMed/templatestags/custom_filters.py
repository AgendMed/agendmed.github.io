from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_names):
    """
    Verifica se o usuário pertence a algum dos grupos fornecidos.
    group_names: String com os nomes dos grupos separados por vírgula.
    """
    return user.groups.filter(name__in=group_names.split(',')).exists()
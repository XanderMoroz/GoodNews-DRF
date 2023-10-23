from django import template

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
register = template.Library()

@register.filter(name='censor')
def censor(value):
    """
    The censor filter replaces the letters of undesirable words
    in titles and article texts with the symbol "*".
    :param value: The value to which the filter needs to be applied
    """
    bad_words = ['профурсетка', 'проходимец', 'охальница', 'негодяй', 'подлец']
    for bad_word in bad_words:
        if bad_word in value:
            value = value.replace(bad_word, '*' * len(bad_word))
    return value

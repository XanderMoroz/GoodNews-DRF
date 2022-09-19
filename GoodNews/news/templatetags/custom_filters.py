

from django import template

register = template.Library()
# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter(name='censor')
def censor(value):
   """ Фильтр censor, который заменяет буквы нежелательных слов
    в заголовках и текстах статей на символ «*».
    value: значение, к которому нужно применить фильтр """
   bad_words = ['профурсетка', 'проходимец', 'охальница', 'сволочь', 'негодяй', 'подлец']
   text = set(value.split())
   for word in text:
      for bad_word in bad_words:
         if word == bad_word:
               return value.replace(word, '*' * len(word))
   return value # Возвращаемое функцией значение подставится в шаблон.
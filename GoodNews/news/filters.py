from django.forms import SelectDateWidget, Select, DateInput
# импортируем filterset, чем-то напоминающий знакомые дженерики
from django_filters import FilterSet, DateFilter
from .models import Post


# создаём фильтры
class PostFilter(FilterSet):
    creation_date = DateFilter(field_name='creation_date',
                               label='Опубликованы позже',
                               lookup_expr='gt', # должна быть позже или равна тому (greater than), что указал пользователь
                               widget=DateInput(format='%d.%m.%Y', attrs={'type': 'date', 'class': 'inp'}))
    """
    post_title = CharFilter(label='Название',
                            lookup_expr='contains') # должно быть похожее на запрос пользователя

    author = CharFilter(label='Автор',
                        lookup_expr='contains') # должно быть похожее на запрос пользователя

    categories = ChoiceFilter(label='Категории',
                        lookup_expr='contains') # должно быть похожее на запрос пользователя

        #ChoiceFilter(label='Категории', widget=Select(attrs={'class': 'inp'}),)

    #"""

    class Meta:
        """
        Здесь в мета классе надо предоставить модель и указать поля,
        по которым будет фильтроваться (т. е. подбираться) информация о публикациях
        """
        model = Post
        # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)
        fields = {'author__user': ['exact'],
                  'post_title': ['icontains'],
                  #'categories': ['contains']
                  }

        """
        fields = ('creation_date',
                  'post_title',
                  'author',
                  'categories')
        """
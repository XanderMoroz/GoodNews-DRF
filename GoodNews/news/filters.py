from django.forms import SelectDateWidget, Select, DateInput
# импортируем filterset, чем-то напоминающий дженерики
from django_filters import FilterSet, DateFilter, CharFilter, ChoiceFilter

# создаём фильтры
class PostFilter(FilterSet):
    author = CharFilter(
        label='Автор',
        lookup_expr='contains'  # должно быть похожее на запрос пользователя
    )
    creation_date = DateFilter(
        field_name='creation_date',
        label='Опубликованы позже',
        lookup_expr='gt',  # должна быть позже или равна тому (greater than), что указал пользователь
        widget=DateInput(format='%d.%m.%Y', attrs={'type': 'date', 'class': 'inp'})
    )
    post_title = CharFilter(
        label='Название',
        lookup_expr='contains'  # должно быть похожее на запрос пользователя
    )
    categories = ChoiceFilter(
        label='Категории',
        choices=[(1, 'Fashion'), (2, 'History '), (3, 'Science'), (4, 'Movies')],
        widget=Select(attrs={'class': 'inp'})
    )

    class Meta:
        """
        Здесь в мета классе надо предоставить модель и указать поля,
        по которым будет фильтроваться (т. е. подбираться) информация о публикациях
        """
        # model = Post

        """
        поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)
        fields = {'author__user': ['exact'],
                  'post_title': ['icontains'],
                  'categories': ['exact']
                  }
        """
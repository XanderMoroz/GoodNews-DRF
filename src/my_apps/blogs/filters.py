from django.forms import DateInput, Select
from django_filters import FilterSet, DateFilter, CharFilter, ChoiceFilter

from src.my_apps.blogs.models import Post


class PostFilter(FilterSet):
    AUTHOR_LOKUP_EXPR = 'contains'
    DATE_LOOKUP_EXPR = 'gt'
    DATE_WIDGET_FORMAT = '%d.%m.%Y'

    author = CharFilter(label='Author', lookup_expr=AUTHOR_LOKUP_EXPR)
    creation_date = DateFilter(
        field_name='creation_date',
        label='Published after',
        lookup_expr=DATE_LOOKUP_EXPR,
        widget=DateInput(format=DATE_WIDGET_FORMAT, attrs={'type': 'date', 'class': 'inp'})
    )
    post_title = CharFilter(label='Title', lookup_expr=AUTHOR_LOKUP_EXPR)
    categories = ChoiceFilter(
        label='Categories',
        choices=[(1, 'Fashion'), (2, 'History'), (3, 'Science'), (4, 'Movies')],
        widget=Select(attrs={'class': 'inp'})
    )

    class Meta:
        """
        Here in the meta class, you need to provide the model and specify the fields,
        by which the information about the posts will be filtered
        """
        model = Post

        fields = {'author__user': ['exact'],
                  'title': ['icontains'],
                  'categories': ['exact']
                  }

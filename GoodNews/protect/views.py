from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        """
        Сначала мы получили весь контекст из класса-родителя, а после добавили новую переменную is_not_authors.
        Чтобы ответить на вопрос, есть ли пользователь в группе, мы заходим в переменную запроса self.request.
        Из этой переменной мы можем вытащить текущего пользователя. В поле groups хранятся группы, в которых он состоит.
        Далее мы применяем фильтр к этим группам и ищем ту самую, имя которой authors.
        После чего проверяем, есть ли какие-то значения в отфильтрованном списке.
        Метод exists() вернёт True, если группа premium в списке групп пользователя найдена, иначе — False.
        :param kwargs:
        :return: boolean
        """
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context
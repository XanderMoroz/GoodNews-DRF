from django.views.generic.edit import CreateView
from .models import RegisterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group


class BaseRegisterView(CreateView):
    """
    Он имеет несколько атрибутов:
    1) модель формы, которую реализует данный дженерик;
    2) форма, которая будет заполняться пользователем;
    3) URL, на который нужно направить пользователя после успешного ввода данных в форму.
    """
    model = User
    form_class = RegisterForm
    success_url = '/'

@login_required
def upgrade_me(request):
    """
    В этом листинге кода мы получили объект текущего пользователя из переменной запроса.
    Вытащили authors-группу из модели Group. Дальше мы проверяем, находится ли пользователь в этой группе
    (вдруг кто-то решил перейти по этому URL, уже будучи автором). И если он всё-таки ещё не в ней — смело добавляем.
    :param request:
    :return:
    """
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')
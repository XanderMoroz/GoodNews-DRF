# Здесь мы импортируем класс формы, который предоставляет allauth
from allauth.account.forms import SignupForm
# Здесь мы импортируем встроенную модель групп
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):
    """
    Чтобы автоматически добавлять пользователя в группу при регистрации, мы должны переопределить только метод save(),
    который выполняется при успешном заполнении формы регистрации.
    """
    def save(self, request):

        user = super(BasicSignupForm, self).save(request)  # Вызываем этот же метод класса-родителя \
        # чтобы необходимые проверки и сохранение в модель User были выполнены.
        basic_group = Group.objects.get(name='common')  # Далее мы получаем объект модели группы basic.
        # Через атрибут user_set, возвращающий список всех пользователей этой группы, мы добавляем нового пользователя в эту группу.
        basic_group.user_set.add(user)
        return user
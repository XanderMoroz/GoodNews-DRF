import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse_lazy
from easy_thumbnails.fields import ThumbnailerImageField


class Author(models.Model):
    '''
    Модель Author, содержащая объекты всех авторов.
    Имеет следующие поля:
    - cвязь «один к одному» с встроенной моделью пользователей User;
    - рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = ThumbnailerImageField(upload_to='images/avatars', blank=True)
    # creation_date = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    author_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


    def update_rating(self) -> str:
        '''
        Метод обновляет рейтинг автора, переданный в аргумент этого метода.
        Он состоит из следующего:
        - суммарный рейтинг каждой статьи автора умножается на 3;
        - суммарный рейтинг всех комментариев автора;
        - суммарный рейтинг всех комментариев к статьям автора.
        :return: User_rating
        '''
        post_rating = self.post_set.all().aggregate(Sum('post_rating')).get('post_rating__sum', 0) * 3
        comment_rating = self.user.comment_set.all().aggregate(Sum('comment_rating')).get('comment_rating__sum', 0)
        news_comments = Post.objects.filter(author=self).values('comment__comment_rating')
        news_comments_rating = sum(rate['comment__comment_rating'] for rate in news_comments)
        self.author_rating = post_rating + comment_rating + news_comments_rating
        self.save()
        return f'{self.author_rating}'

    def get_absolute_url(self):
        # после создания переадресовать в личный кабинет
        return reverse_lazy('profile')

    def __str__(self):
        return f'{self.user}'

class Category(models.Model):
    '''
    Модель Category — темы, которые они отражают (спорт, политика, образование и т. д.).
    Имеет:
    - название категории. Поле должно быть уникальным (параметр unique = True).
    - связь «многие ко многим» с моделью User.
    '''
    title = models.CharField(verbose_name='Название', max_length=256, unique=True)
    image = models.ImageField(upload_to='images/categories', default=None, verbose_name='Картинка категории')
    subscribers = models.ManyToManyField(User, through='UserCategory')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.title}'

    def get_subscribers_emails(self):
        result = set()
        for user in self.subscribers.all():
            result.add(user.email)
        return result

class Post(models.Model):
    '''
    Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    Каждый объект может иметь одну или несколько категорий.
    Модель должна включать следующие поля:
    - связь «один ко многим» с моделью Author;
    - поле с выбором — «статья» или «новость»;
    - автоматически добавляемая дата и время создания;
    - связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    - заголовок статьи/новости;
    - текст статьи/новости;
    - рейтинг статьи/новости.
    '''
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(verbose_name='Тип публикации', max_length=3,
                                 choices=[('ART', 'Article'), ('NEW', 'News')],
                                 default='A')
    creation_date = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory',
                                        verbose_name='Категории',
                                        related_name="post_categories")
    title = models.CharField(verbose_name='Название', max_length=255)
    text = models.TextField(verbose_name='Текст')
    post_rating = models.IntegerField(verbose_name='Рейтинг', default=0)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return f'{self.title} {self.author}'

    def get_absolute_url(self):
        return reverse_lazy('profile')

    def like(self) -> None:
        '''
        Метод, который увеличивает рейтинг на единицу.
        '''
        self.post_rating += 1
        self.save()

    def dislike(self) -> None:
        '''
        Метод, который уменьшает рейтинг на единицу.
        '''
        self.post_rating -= 1
        self.save()

    def preview(self) -> str:
        '''
        Метод возвращает начало статьи (предварительный просмотр)
        длиной 124 символа и добавляет многоточие в конце.
        '''
        pre_text = 124 if len(self.post_text) > 124 else len(self.post_text)
        return self.post_text[:pre_text]+'...'

    def preview20(self) -> str:
        '''
        Метод возвращает начало статьи (предварительный просмотр)
        длиной 20 символов и добавляет многоточие в конце.
        '''
        pre_text = 20 if len(self.text) > 20 else len(self.text)
        return self.text[:pre_text]+'...'


class PostCategory(models.Model):
    '''
    Модель для связи «многие ко многим»:
    - связь «один ко многим» с моделью Post;
    - связь «один ко многим» с моделью Category.
    '''
    post = models.ForeignKey(Post,
                             verbose_name='Публикация',
                             on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Публикация категории'
        verbose_name_plural = 'Публикации категории'

class Comment(models.Model):
    '''
    Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
    Модель будет иметь следующие поля:
    - связь «один ко многим» с моделью Post;
    - связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь);
    - текст комментария;
    - дата и время создания комментария;
    - рейтинг комментария.
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)
    comment_rating = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def get_absolute_url(self):
        # после создания комментария остаться на той же странице
        return reverse_lazy('post_detail', args=[str(self.post.id)])

    def like(self):
        '''
        Метод, который увеличивает рейтинг на единицу.
        '''
        self.comment_rating += 1
        self.save()

    def dislike(self):
        '''
        Метод, который уменьшает рейтинг на единицу.
        '''
        self.comment_rating -= 1
        self.save()

class UserCategory(models.Model):
    '''
    Модель для связи «многие ко многим»:
    - связь «один ко многим» с моделью User;
    - связь «один ко многим» с моделью Category.
    '''
    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 related_name='user_category',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка на категорию'
        verbose_name_plural = 'Подписки на категорию'

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    '''
    Модель Author, содержащая объекты всех авторов.
    Имеет следующие поля:
    - cвязь «один к одному» с встроенной моделью пользователей User;
    - рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        '''
        Метод обновляет рейтинг пользователя, переданный в аргумент этого метода. Он состоит из следующего:
        - суммарный рейтинг каждой статьи автора умножается на 3;
        - суммарный рейтинг всех комментариев автора;
        - суммарный рейтинг всех комментариев к статьям автора.
        :return: user_rating
        '''
        post_rating = self.post_set.all().aggregate(Sum('post_rating')).get('post_rating__sum', 0) * 3
        comment_rating = self.user.comment_set.all().aggregate(Sum('comment_rating')).get('comment_rating__sum', 0)
        news_comments = Post.objects.filter(author=self).values('comment__comment_rating')
        news_comments_rating = sum(rate['comment__comment_rating'] for rate in news_comments)
        self.user_rating = post_rating + comment_rating + news_comments_rating
        self.save()
        return f'{self.user_rating}'

    def __str__(self):
        return f'{self.user}'

class Category(models.Model):
    '''
    Модель Category — темы, которые они отражают (спорт, политика, образование и т. д.).
    Имеет единственное поле:
    - название категории. Поле должно быть уникальным (параметр unique = True).
    '''
    category_name = models.CharField(max_length=256, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f'{self.category_name}'

    def get_subscribers_emails(self):
        result = set()
        for user in self.subscribers.all():
            result.add(user.email)
        return result

class Post(models.Model):
    '''
    Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    Каждый объект может иметь одну или несколько категорий. Модель должна включать следующие поля:
    - связь «один ко многим» с моделью Author;
    - поле с выбором — «статья» или «новость»;
    - автоматически добавляемая дата и время создания;
    - связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    - заголовок статьи/новости;
    - текст статьи/новости;
    - рейтинг статьи/новости.
    '''
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=3, choices=[('ART', 'Article'), ('NEW', 'News')], default='A')
    creation_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.post_title} {self.author}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def like(self):
        '''
        Метод который увеличивает рейтинг на единицу.
        '''
        self.post_rating += 1
        self.save()

    def dislike(self):
        '''
        Метод который уменьшает рейтинг на единицу.
        '''
        self.post_rating -= 1
        self.save()

    def preview(self):
        '''
        Метод возвращает начало статьи (предварительный просмотр)
        длиной 124 символа и добавляет многоточие в конце.
        '''
        pre_text = 124 if len(self.post_text) > 124 else len(self.post_text)
        return self.post_text[:pre_text]+'...'

    def preview20(self):
        '''
        Метод возвращает начало статьи (предварительный просмотр)
        длиной 20 символов и добавляет многоточие в конце.
        '''
        pre_text = 20 if len(self.post_text) > 20 else len(self.post_text)
        return self.post_text[:pre_text]+'...'


class PostCategory(models.Model):
    '''
    Модель для связи «многие ко многим»:
    - связь «один ко многим» с моделью Post;
    - связь «один ко многим» с моделью Category.
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date_comment = models.DateTimeField(auto_now_add=True)
    comment_text = models.CharField(max_length=256)
    comment_rating = models.FloatField(default=0)

    def like(self):
        '''
        Метод который увеличивает рейтинг на единицу.
        '''
        self.comment_rating += 1
        self.save()

    def dislike(self):
        '''
        Метод который уменьшает рейтинг на единицу.
        '''
        self.comment_rating -= 1
        self.save()

class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='user_category')
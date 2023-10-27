from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField


class Author(models.Model):
    """
    Represents an author.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author")
    photo = ThumbnailerImageField(upload_to='images/avatars', blank=True)
    creation_date = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    author_rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('profile')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self) -> str:
        """
        Updates the author's rating based on post ratings, comment ratings, and news comment ratings.

        Returns:
            str: The updated author rating.
        """
        post_rating = self.posts.aggregate(Sum('post_rating')).get('post_rating__sum', 0) * 3
        comment_rating = self.user.comments.aggregate(Sum('comment_rating')).get('comment_rating__sum', 0)
        news_comments = self.posts.values('comments__comment_rating')
        news_comments_rating = sum(rate['comments__comment_rating'] for rate in news_comments)
        self.author_rating = post_rating + comment_rating + news_comments_rating
        self.save()
        return f'{self.author_rating}'

    def __str__(self):
        """
        Returns a string representation of the author.

        Returns:
            str: The user's username.
        """
        return f'{self.user}'


class Category(models.Model):
    """
    Represents a category.
    """
    title = models.CharField(verbose_name='Title', max_length=256, unique=True)
    image = models.ImageField(upload_to='images/categories', default=None, verbose_name='Category Image')
    subscribers = models.ManyToManyField(User, through='UserCategory', related_name="categories")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """
        Returns a string representation of the category.

        Returns:
            str: The title of the category.
        """
        return f'{self.title}'

    def get_subscribers_emails(self):
        """
        Returns a set of email addresses of subscribers to the category.

        Returns:
            set: Set of email addresses.
        """
        return {user.email for user in self.subscribers.all()}


class Post(models.Model):
    """
    Represents a post.
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(verbose_name='Title', max_length=255)
    text = models.TextField(verbose_name='Text')
    type = models.CharField(verbose_name='Publication Status', max_length=3,
                            choices=[('PUB', 'Published'), ('UPB', 'Unpublished')],
                            default='PUB')
    creation_date = models.DateTimeField(verbose_name='Creation Time', auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory', related_name="posts")
    post_rating = models.IntegerField(verbose_name='Rating', default=0)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        """
        Returns a string representation of the post.

        Returns:
            str: The title of the post and the name of the author.
        """
        return f'{self.title} by {self.author}'

    def like(self):
        """
        Increases the rating of the post by 1 and saves the changes.
        """
        self.post_rating += 1
        self.save()

    def dislike(self):
        """
        Decreases the rating of the post by 1 and saves the changes.
        """
        self.post_rating -= 1
        self.save()

    def preview(self, length=124):
        """
        Returns a preview of the post text with the specified length.

        Args:
            length (int): The length of the preview text (default is 124).

        Returns:
            str: The preview of the post text.
        """
        return f'{self.text[:length]}...'


class PostCategory(models.Model):
    """
    Represents the relationship between a post and a category.
    """
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE, related_name="post_categories")
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE, related_name="post_categories")

    class Meta:
        verbose_name = 'Публикация категории'
        verbose_name_plural = 'Публикации категории'


class Comment(models.Model):
    """
    Represents a comment made by a user on a post.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)
    comment_rating = models.DecimalField(default=0, max_digits=5, decimal_places=1)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        """
        Increases the rating of the comment by 1 and saves the changes.
        """
        self.comment_rating += 1
        self.save()

    def dislike(self):
        """
        Decreases the rating of the comment by 1 and saves the changes.
        """
        self.comment_rating -= 1
        self.save()


class UserCategory(models.Model):
    """
    Represents the relationship between a user and a category for subscription.
    """
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, related_name="user_categories")
    category = models.ForeignKey(Category, verbose_name='Category', related_name='user_categories', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка на категорию'
        verbose_name_plural = 'Подписки на категорию'
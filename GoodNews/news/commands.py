
from django.contrib.auth.models import User
#from news.models import Author, Category, Post, PostCategory, Comment
from news.models import Post, PostCategory, Category, Comment, Author

import random

def todo():
    #1 ЗАДАЧА: Создать двух пользователей (с помощью метода User.objects.create_user('username')).
    user1 = User.objects.create_user(username="Olaf Balke", email='Olaf_Balke@gmail.com', password='12345')
    user2 = User.objects.create_user(username="Leia Seidu", email='Leia_Seidu@gmail.com', password='qwerty')
    user3 = User.objects.create_user(username="Tom Crowter", email='Leia_Seidu@mail.ru', password='asdfg')
    #2 РЕЗУЛЬТАТ: Пользователи (user1, user2, user3) созданы.

    #3 ЗАДАЧА: Создать два объекта модели Author, связанные с пользователями.
    author1 = Author.objects.create(user=user1)
    author2 = Author.objects.create(user=user2)
    #3 РЕЗУЛЬТАТ: Авторы (author1, author2) созданы.


    #4 ЗАДАЧА: Добавить 4 категории в модель Category.
    category_movies = Category.objects.create(category_name="Movies")
    category_fashion = Category.objects.create(category_name="Fashion")
    category_history = Category.objects.create(category_name="History")
    category_science = Category.objects.create(category_name="Science")
    #4 РЕЗУЛЬТАТ: Категории (category_movies, category_fashion, category_history, category_science) созданы.

    #5 ЗАДАЧА: Добавить 2 статьи и 1 новость.
    post1 = Post.objects.create(post_type='ART',
                                author=author1,
                                post_title='Who was Johanes Gutenberg',
                                post_text='Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo\
                                       ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis\
                                        parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec,\
                                         pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.\
                                          Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu.\
                                           In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.\
                                            Nullam dictum felis eu pede mollis pretium. Integer tincidunt.\
                                             Cras dapibus. Vivamus elementum semper nisi.\
                                              Aenean vulputate eleifend tellus.')

    post2 = Post.objects.create(post_type='ART',
                                author=author2,
                                post_title='Bedlam: The story most infamous Asylum',
                                post_text='Maecenas malesuada. Praesent congue erat at massa.\
                                       Sed cursus turpis vitae tortor. Donec posuere vulputate arcu.\
                                        Vestibulum ante ipsum primis in faucibus orci luctus et ultrices\
                                         posuere cubilia Curae; Sed aliquam, nisi quis porttitor congue,\
                                          elit erat euismod orci, ac placerat dolor lectus quis orci.\
                                           Phasellus consectetuer vestibulum elit. Aenean tellus metus,\
                                            bibendum sed, posuere ac, mattis non, nunc.\
                                             Vestibulum fringilla pede sit amet augue. In turpis.\
                                              Pellentesque posuere. Praesent turpis. Aenean posuere,\
                                               tortor sed cursus feugiat, nunc augue blandit nunc,\
                                                eu sollicitudin urna dolor sagittis lacus. Donec elit libero,\
                                                 sodales nec, volutpat a, suscipit non, turpis. Nullam sagittis.')

    post3 = Post.objects.create(post_type='NEW',
                                author=author2,
                                post_title='Item of the week: The Little Black Dress',
                                post_text='Nam ipsum risus, rutrum vitae, vestibulum eu, molestie vel, lacus.\
                                       Sed augue ipsum, egestas nec, vestibulum et, malesuada adipiscing, dui.\
                                        Vestibulum facilisis, purus nec pulvinar iaculis, ligula mi congue nunc,\
                                         vitae euismod ligula urna in dolor. Mauris sollicitudin fermentum libero.\
                                          Praesent nonummy mi in odio. Nunc interdum lacus sit amet orci.\
                                           Vestibulum rutrum, mi nec elementum vehicula, eros quam gravida nisl,\
                                            id fringilla neque ante vel mi. Morbi mollis tellus ac sapien.\
                                             Phasellus volutpat, metus eget egestas mollis, lacus lacus blandit dui,\
                                              id egestas quam mauris ut lacus. Sed in libero ut nibh accumsan.')
    #5 РЕЗУЛЬТАТ: 2 статьи (post1, post2) и 1 новость (post3) созданы.

    #6 ЗАДАЧА: Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
    PostCategory.objects.create(post=post1, category=category_movies)
    PostCategory.objects.create(post=post1, category=category_history)

    PostCategory.objects.create(post=post2, category=category_history)
    PostCategory.objects.create(post=post2, category=category_science)

    PostCategory.objects.create(post=post3, category=category_fashion)
    #5 РЕЗУЛЬТАТ: 2 статьям (post1, post2) присвоены по 2 категории, 1 новости (post3) присвоена 1 категория.

    #6 ЗАДАЧА: Создать как минимум 4 комментария к разным объектам Post (в каждом объекте - как минимум один комментарий).

    comment1 = Comment.objects.create(comment_post=post2,
                                      comment_user=user2,
                                      comment_text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem \
                                       accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo\
                                        inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.')

    comment2 = Comment.objects.create(comment_post=post2,
                                      comment_user=user1,
                                      comment_text='Nemo enim ipsam voluptatem quia voluptas sit aspernatur!')

    comment3 = Comment.objects.create(comment_post=post1,
                                      comment_user=user2,
                                      comment_text='Sed augue ipsum, egestas nec, vestibulum et, malesuada adipiscing, dui.')

    comment4 = Comment.objects.create(comment_post=post1,
                                      comment_user=user1,
                                      comment_text='Sed cursus turpis vitae tortor. Donec posuere vulputate arcu.')

    comment5 = Comment.objects.create(comment_post=post3,
                                      comment_user=user3,
                                      comment_text='Ut enim ad minima veniam, quis nostrum exercitationem ullam\
                                       corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?')

    comment6 = Comment.objects.create(comment_post=post2,
                                      comment_user=user3,
                                      comment_text='Vestibulum fringilla pede sit amet augue. In turpis.')

    comment7 = Comment.objects.create(comment_post=post3,
                                      comment_user=user1,
                                      comment_text='Pellentesque posuere.)) Praesent turpis!!')
    #6 РЕЗУЛЬТАТ: Создано 7 комментариев.

    #7 ЗАДАЧА: Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги.
    random_choice_list = [post1, post2, post3,
                          comment1, comment2, comment3, comment4, comment5, comment6, comment7]
    for i in range(100):
        rand_obj = random.choice(random_choice_list)
        if i % 2:
            rand_obj.like()
        else:
            rand_obj.dislike()


    #7 РЕЗУЛЬТАТ: Рейтинги статьей/новостей и комментариев скорректированы.

    #8 ЗАДАЧА: Обновить рейтинги пользователей.
    Author.objects.get(pk=1).update_rating()
    Author.objects.get(pk=2).update_rating()
    #8 РЕЗУЛЬТАТ: Pейтинги пользователей (user1, user2) обновлены.

    #9 ЗАДАЧА: Вывести username и рейтинг лучшего пользователя (сортировка и поле первого объекта).
    most_rated_author = Author.objects.all().order_by('-user_rating')[0].user.username
    print('Мost rated author is', most_rated_author)
    #9 РЕЗУЛЬТАТ: username и рейтинг лучшего пользователя определен и выведен.

    #10 ЗАДАЧА: Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи.
    best_article = Post.objects.filter(post_type='ART').order_by('-post_rating')[0]
    best_article_rating = best_article.post_rating
    best_article_time = best_article.creation_date
    best_article_author = best_article.author.user.username
    best_article_preview = best_article.preview()
    best_article_title = best_article.post_title
    print(f'The best article written by {best_article_author} at {best_article_time}.\n'
          f'It is entitled {best_article_title} and has the biggest rating {best_article_rating} points.\n'
          f'Preview: {best_article_preview}')
    #10 РЕЗУЛЬТАТ: Дата добавления, username автора, рейтинг, заголовок и превью лучшей статьи (best_article) выведены.

    #11 ЗАДАЧА: Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
    for comment in Comment.objects.filter(comment_post=best_article):
        print( f'Comment id: {comment.id}, \n'
               f'Data: {comment.creation_date_comment}, \n'
               f'Username: {comment.comment_user.username}, \n'
               f'Rating: {comment.comment_rating}, \n'
               f'Comment: {comment.comment_text}')
    #11 РЕЗУЛЬТАТ: Все комментарии к лучшей статье (best_article) выведены.
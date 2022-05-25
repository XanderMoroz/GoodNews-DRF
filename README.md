<p dir="auto" data-sourcepos="2:1-3:171">Итоговое задание этого модуля заключается в создании этого приложения в котором должно быть:</p>
<ul style="list-style-type: circle;">
<li>1.1 Модель <strong><em>Author</em></strong>(<span style="color: #339966;">готово</span>)</li>
<li>1.2 Модель <strong><em>Category</em></strong>(<span style="color: #339966;">готово</span>)</li>
<li>1.3 Модель <strong><em>Post</em></strong>(<span style="color: #339966;">готово</span>)</li>
<li>1.4 Модель <strong><em>PostCategory</em></strong>(<span style="color: #339966;">готово</span>)</li>
<li>1.5 Модель <strong><em>Comment</em></strong>(<span style="color: #339966;">готово</span>)</li>
</ul>
<p dir="auto" data-sourcepos="11:1-11:47"><em>Что надо сделать в Django Shell?</em></p>
<ol>
<li dir="auto" data-sourcepos="13:1-23:149">Создать двух пользователей (с помощью метода User.objects.create_user('username')).(<span style="color: #339966;">готово</span>)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Создать два объекта модели Author, связанные с пользователями.(<span style="color: #339966;">готово</span>)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Добавить 4 категории в модель Category.(<span style="color: #339966;">готово</span>)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Добавить 2 статьи и 1 новость.(<span style="color: #339966;">готово</span>)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).(<span style="color: #339966;">готово</span>)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).(<span style="color: #339966;">готово</span>)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.(<span style="color: #339966;">готово</span>)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Обновить рейтинги пользователей.(<span style="color: #339966;">готово</span>)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).(готово)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.(<span style="color: #339966;">готово</span>)</li>
<li dir="auto" data-sourcepos="13:1-23:149">Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.(<span style="color: #339966;">готово</span>)</li>
</ol>

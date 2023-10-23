
from django.contrib.postgres.search import SearchVector

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import CreateView, FormMixin

from .forms import PostForm, CategoryForm, CommentForm
from .models import Post, Category, Author, PostCategory, Comment  # импорт нашей модели
from .filters import PostFilter  # импорт нашего фильтра
from .signals import check_post_limits


class MainView(TemplateView):
    """
    Represents the main view for the blogs.
    """
    template_name = 'blogs/main.html'

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the main view.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context['main_post'], _ = self.get_random_post_with_category()
        context['secondary_post1'], context['post_cat1'] = self.get_random_post_with_category()
        context['secondary_post2'], context['post_cat2'] = self.get_random_post_with_category()
        context['latest_posts'] = Post.objects.order_by('creation_date')[:4]
        context['list_of_categories'] = Category.objects.all()
        return context

    def get_random_post_with_category(self):
        """
        Retrieves a random post with its associated category.

        Returns:
            tuple: A tuple containing the random post and its associated category.
        """
        post = Post.objects.order_by('?').first()
        post_category = PostCategory.objects.filter(post=post)
        return post, post_category


class Search(ListView):
    """
    Represents the search view for posts.
    """
    model = Post
    template_name = 'blogs/post_search.html'
    context_object_name = 'search_list'
    ordering = '-creation_date'
    paginate_by = 10
    vector = SearchVector('title', 'text', config='russian')

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the search view.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        user_search_request = self.request.GET.get("query")
        # Fetch posts whose title or text matches the query
        context['search_res'] = Post.objects.annotate(
            search=self.vector
        ).filter(search=user_search_request)
        return context

    def get_queryset(self):
        """
        Retrieves the queryset for the search view.

        Returns:
            QuerySet: The filtered queryset.
        """
        return PostFilter(self.request.GET, queryset=super().get_queryset()).qs


class PostDetail(DetailView):
    """
    Represents the view for displaying the details of a post.
    """
    model = Post
    template_name = 'blogs/post_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the search view.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)

        # Get the post ID
        post_id = self.kwargs.get('pk')

        # Get the comments related to the post
        comments = Comment.objects.filter(post=post_id)

        # Get unique users from the comments
        unique_users = set(comment.user for comment in comments)

        # Get author's photos
        avatar_dict = {user.id: Author.objects.filter(user=user).first().photo for user in unique_users}

        context.update({
            'comments': comments,
            'avatar_dict': avatar_dict
        })

        return context


class PostCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Класс представления для создания статьи.
    Наследован от встроенного дженерика, миксина требующего авторизацию и миксина, требующего право доступа
    """
    permission_required = ('news.add_post',)
    template_name = 'blogs/cruds/create_post.html'
    form_class = PostForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        author = Author.objects.get(user_id=user.pk)
        initial['author'] = author
        return initial

    def post(self, request, *args, **kwargs):
        new_post = Post(
            type=request.POST['type'],
            text=request.POST['text'],
            title=request.POST['title'],
            author_id=request.POST['author'],
                        )
        if check_post_limits(sender=Post, instance=new_post, **kwargs) < 3:
            new_post.save()
            new_post.categories.add(request.POST.get('categories'))

        return redirect('profile')


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    View class for editing a post.
    Inherits from the built-in generic view, mixin requiring authorization and mixin requiring access rights.
    """
    permission_required = ('news.change_post',)
    template_name = 'blogs/cruds/edit_post.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        """
        The get_object method we use instead of queryset to get information about the object
        that we are going to edit.
        :param kwargs:
        :return: Post class object
        """
        return Post.objects.get(pk=self.kwargs.get('pk'))


class PostDeleteView(DeleteView):
    """
    View class for deleting a post.
    Inherits from the built-in generic view.
    """
    template_name = 'blogs/cruds/delete_post.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('profile')

@login_required
def subscribe(request, **kwargs):
    """
    Subscribes the logged-in user to a category.

    Args:
        request (HttpRequest): The HTTP request object.
        **kwargs: Additional keyword arguments.

    Returns:
        HttpResponse: A redirect response.

    Raises:
        Category.DoesNotExist: If the specified category does not exist.
    """
    category = Category.objects.get(pk=kwargs['pk'])
    user = request.user
    if user not in category.subscribers.all():
        category.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unsubscribe(request, **kwargs):
    """
    Unsubscribes the logged-in user from a category.

    Args:
        request (HttpRequest): The HTTP request object.
        **kwargs: Additional keyword arguments.

    Returns:
        HttpResponse: A redirect response.

    Raises:
        Category.DoesNotExist: If the specified category does not exist.
    """
    category = Category.objects.get(pk=kwargs['pk'])
    user = request.user
    if user in category.subscribers.all():
        category.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


class CategoriesSubscription(ListView, FormMixin):
    """
    View for subscribing to categories.
    """
    model = Category
    template_name = 'blogs/subscription.html'
    context_object_name = 'subscription'
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        """
        Get the context data for the category subscription view.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        list_of_categories = Category.objects.all()
        context['list_of_categories'] = list_of_categories
        post_dict = {}
        for cat in list_of_categories:
            posts_of_category = PostCategory.objects.filter(category=cat)
            post_dict[cat.pk] = posts_of_category.count()
        context['post_dict'] = post_dict
        category_comments = {}
        for category in list_of_categories:
            comment_counts = Post.objects.filter(
                categories__id=category.pk
            ).annotate(num_comments=Count('comment'))
            category_comments[category.pk] = comment_counts
        context['category_comments'] = category_comments
        return context


class PostsOfCategory(ListView):
    """
    View for displaying posts of a specific category.
    """
    model = Post
    template_name = 'blogs/posts_of_category.html'
    context_object_name = 'posts_of_category'
    ordering = '-creation_date'
    paginate_by = 1

    def get_queryset(self):
        """
        Get the queryset for fetching posts of a specific category.

        Returns:
            QuerySet: The filtered queryset.
        """
        category_id = self.kwargs['pk']
        category = Category.objects.get(id=category_id)
        queryset = super().get_queryset()
        return queryset.filter(categories=category)

    def get_context_data(self, **kwargs):
        """
        Get the context data for displaying posts of a specific category.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        current_category = Category.objects.get(id=category_id)
        context['current_category'] = current_category
        return context


class CommentCreateView(CreateView, LoginRequiredMixin):
    """
    View for creating a comment.
    """
    model = Comment
    template_name = 'blogs/cruds/create_comment.html'
    form_class = CommentForm

    def get_initial(self):
        """
        Get the initial data for the comment creation form.

        Returns:
            dict: The initial data.
        """
        initial = super().get_initial()
        current_user = self.request.user
        initial['user'] = current_user
        post_id = self.kwargs['post_id']
        comment_post = Post.objects.filter(id=post_id).first()
        initial['post'] = comment_post
        comment_text = "This article is awesome!"
        initial['text'] = comment_text
        return initial

    def get_context_data(self, **kwargs):
        """
        Get the context data for the comment creation view.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        current_author = Author.objects.get(user=current_user)
        context['current_author'] = current_author
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request for creating a comment.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response.
        """
        current_user = request.user
        post_id = self.kwargs['post_id']
        comment_post = Post.objects.filter(id=post_id).first()
        new_comment = Comment(
            user=current_user,
            post=comment_post,
            text=request.POST['text'],
        )
        new_comment.save()
        return redirect('post_detail', pk=comment_post.id)
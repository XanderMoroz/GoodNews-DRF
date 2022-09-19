from django.contrib import admin
from .models import Category, Post, Author, PostCategory

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
# Register your models here.

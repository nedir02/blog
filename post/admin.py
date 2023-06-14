from django.contrib import admin

# Register your models here.
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'published_date', 'slug'] #adminka bolumde gorkeziljek bolumler
    list_display_links = ['content', 'published_date'] #adminkada bolumlere link goymak
    list_filter = ['published_date'] #adminkada yorite filtr doretmek
    search_fields = ['title', 'content'] #adminkada gozleg bolumi
    list_editable = ['title'] #adminkada bolumi uytgetmek

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)

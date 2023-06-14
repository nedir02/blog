from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey('auth.User', verbose_name="Yazar", on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=120, verbose_name="Baslik")
    content = RichTextField(verbose_name="Icerik")
    published_date = models.DateTimeField(verbose_name="yayinlanma tarihi", auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=130)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={
            'slug': self.slug})  # dinamicny absolute url adres posts; post:detail dp yazmagymyzyn sebabi beyleki app-da detailda konfilt bermez yaly onun ucin ilki url posts-da app name gorkezmeli
        # return "/post/{}".format(self.id)

    def get_create_url(self):
        return reverse('post:create')

    def get_update_url(self):
        return reverse('post:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post:delete', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-published_date", 'id']


class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Isim")
    content = models.TextField(verbose_name="Yorum")
    created_date = models.DateTimeField(auto_now_add=True)

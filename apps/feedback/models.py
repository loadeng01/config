from django.db import models

from apps.post.models import Post


class Like(models.Model):
    owner = models.ForeignKey('auth.User', related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.is_liked} --> {self.post}'


class Favorites(models.Model):
    owner = models.ForeignKey('auth.user', related_name='favorites', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('owner', 'post')





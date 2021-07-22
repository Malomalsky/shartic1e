from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    header = models.CharField(max_length=400)
    url = models.URLField(verbose_name='url', unique=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='date')

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-date_added']


class ShortDescription(models.Model):
    """
    Модель краткого содержания
    """
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='short')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='short', auto_created=True)
    text = models.CharField(max_length=10000, blank=False)
    date_added = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='sharticle_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='sharticle_dislikes', blank=True)

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_dislikes(self):
        return self.dislikes.count()

    @property
    def rating(self):
        """
        Относительный рейтинг краткого содержания - соотношение лайков и дизлайков.
        Желательно сортировать по этому параметру.
        """
        return self.total_likes - self.total_dislikes

    def __str__(self):
        return self.author.get_username() + " | " + self.text[:30] + "..."

    class Meta:
        verbose_name = 'Краткое содержание'
        verbose_name_plural = 'Краткие содержания'

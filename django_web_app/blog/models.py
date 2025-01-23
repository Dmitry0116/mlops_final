from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os

class Post(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(null=True, blank=True, upload_to='Files')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_posted']  # Сортировка постов по дате (новые сначала)

    def __str__(self):
        return self.title

    def extension(self):
        """Возвращает расширение файла."""
        return os.path.splitext(self.file.name)[1] if self.file else ''

    def get_absolute_url(self):
        """Возвращает URL для доступа к данному посту."""
        return reverse('post-detail', kwargs={'pk': self.pk})


from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Сначала сохраняем объект, чтобы получить доступ к изображению
        super(Profile, self).save(*args, **kwargs)

        # Открываем изображение
        img = Image.open(self.image.path)

        # Проверяем размеры изображения и изменяем его, если необходимо
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    # Добавим метод для создания или обновления профиля
    @staticmethod
    def create_or_update_profile(user):
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

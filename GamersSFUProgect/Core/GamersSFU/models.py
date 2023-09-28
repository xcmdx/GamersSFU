

# Название игры (game_title) - название игры, например, "Dota 2" или "The Witcher 3: Wild Hunt".

# Описание игры (game_description) - краткое описание игры, которое рассказывает о сюжете, механике игры и основных особенностях.

# Изображение игры (game_image) - ссылка или путь к изображению, представляющему игру, таким образом, пользователи могут увидеть превью или обложку.

# Разработчик (developer) - данные о компании, ответственной за разработку игры.

# Жанр (genre) - указание на жанр игры, такой как экшн, ролевая игра, стратегия и т.д.

# (потом добавлю) Системные требования (system_requirements) - информация о минимальных и рекомендуемых системных требованиях для запуска игры, включая операционную систему, процессор, видеокарту и объем ОЗУ.

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class MyUsers(AbstractBaseUser, PermissionsMixin):
    role = models.CharField(max_length=255, blank=True, null=True)
    Login = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, blank=True, null=True)
#    password = models.CharField(max_length=255, blank=False, null=False)
#    role = models.PositiveIntegerField(default=1)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_developer = models.BooleanField(default=False)

    is_moderator = models.BooleanField(default=False)

    USERNAME_FIELD = 'Login'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    is_blocked = models.BooleanField(default=False)

    date_create = models.DateTimeField(auto_now_add=True)
    #phone = models.CharField(max_length=11, null=True)
    class Meta:
        verbose_name = 'Пользователи'
        ordering = [ 'date_create' ]
    def __str__(self):
        return 'Пользователь: {}'.format(self.Login)


# фвйлы игры в zip формате
class ZipFile(models.Model):
    File = models.FileField(upload_to="./static/zip_files/")

    class Meta:
        verbose_name = 'Файлы игр'
        ordering = [ 'id' ]
    
    def __str__(self):
        return f"{self.File.name}"
    
# жанры игр
class Genre(models.Model):
    Genre = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Жанры игр'
        ordering = [ 'id' ]
    
    def __str__(self):
        return f"{self.Genre}"
    
# изображения игр
class GameImage(models.Model):
    ImageFile = models.FileField(upload_to="./static/img/")

    class Meta:
        verbose_name = 'Жанры игр'
        ordering = [ 'id' ]
    
    def __str__(self):
        return f"{self.ImageFile.name}"

# страница игры
class Game(models.Model):

    Title = models.CharField(max_length=255)

    Description = models.CharField(max_length=1024)

    GameFile = models.ForeignKey(ZipFile, on_delete=models.CASCADE, null=False)

    Developer = models.ForeignKey(MyUsers, on_delete=models.DO_NOTHING, null=False)

    class Meta:
        verbose_name = 'Стрыницы игр'
        ordering = [ 'id' ]
    
    def __str__(self):
        return f"{self.Title}"

# смежная таблица объединяющая игры и жанры 
class GameGanre(models.Model):
    Game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, null=False)
    Genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING, null=False)

    class Meta:
        verbose_name = 'Игры связанные с жанрами'
    
    # def __str__(self):
    #     return f"{self.Game.Title} {self.Genre.name}"


# смежная таблица объединяющая игры и изображения
class GamePostImage(models.Model):
    Game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, null=False)
    GameImage = models.ForeignKey(GameImage, on_delete=models.DO_NOTHING, null=False)

    class Meta:
        verbose_name = 'Игры связанные с изображениями'
    
    # def __str__(self):
    #     return f"{self.Game.Title} {self.GameImage.name}"
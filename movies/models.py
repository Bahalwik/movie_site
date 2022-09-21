from django.db import models
from datetime import date
from django.urls import reverse


class Category(models.Model):
    """"Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Актёры и режиссёры"""
    name = models.CharField("Имя", max_length=150)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Актёр или режиссёр"
        verbose_name_plural = "Актёры и режиссёры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Жанр", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Film(models.Model):
    """Фильм"""
    title = models.CharField("Фильм", max_length=150)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies")
    year = models.PositiveSmallIntegerField("Дата выхода", default="-")
    country = models.CharField("Страна", max_length=50)
    directors = models.ManyToManyField(Actor, verbose_name="режиссёр", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="Актёр", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    world_premiere = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="Сумма в долларах")
    fees_in_USA = models.PositiveIntegerField("сборы в Америке", default=0, help_text="Сумма в долларах")
    fees_in_world = models.PositiveIntegerField("сборы в мире", default=0, help_text="Сумма в долларах")
    category = models.ForeignKey(Category, verbose_name="категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    trailer = models.TextField("Трейлер к фильму на YouTube", default='',
                               help_text='Пример https://www.youtube.com/embed/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Film, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звёзды рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звёзда рейтинга"
        verbose_name_plural = "Звёзды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг фильма"""
    ip = models.CharField("IP адресата", max_length=20)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звёзд")
    movie = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="Фильм")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы к фильму"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=50)
    text = models.TextField("Комментарий", max_length=3000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="фильм")

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


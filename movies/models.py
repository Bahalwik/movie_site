from django.db import models
from datetime import date
from django.urls import reverse


class Category(models.Model):
    """"Categories"""
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    """Actors and directors"""
    name = models.CharField("Имя", max_length=150)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Actor and director"
        verbose_name_plural = "Actors and directors"


class Genre(models.Model):
    """Genres"""
    name = models.CharField("Genre", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Film(models.Model):
    """Film"""
    title = models.CharField("Film", max_length=150)
    tagline = models.CharField("tagline", max_length=100, default='')
    description = models.TextField("Description")
    poster = models.ImageField("poster", upload_to="movies")
    year = models.PositiveSmallIntegerField("year", default="-")
    country = models.CharField("country", max_length=50)
    directors = models.ManyToManyField(Actor, verbose_name="director", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="actors", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="genres")
    world_premiere = models.DateField("world_premiere", default=date.today)
    budget = models.PositiveIntegerField("budget", default=0, help_text="Amount in dollars")
    fees_in_USA = models.PositiveIntegerField("fees_in_USA", default=0, help_text="Amount in dollars")
    fees_in_world = models.PositiveIntegerField("fees_in_world", default=0, help_text="Amount in dollars")
    category = models.ForeignKey(Category, verbose_name="category", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField("draft", default=False)
    trailer = models.TextField("Trailer for the movie on YouTube", default='',
                               help_text='Example https://www.youtube.com/embed/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Films"


class MovieShots(models.Model):
    """Stills from the film"""
    title = models.CharField("title", max_length=100)
    description = models.TextField("description")
    image = models.ImageField("image", upload_to="movie_shots/")
    movie = models.ForeignKey(Film, verbose_name="Film", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Stills from the film"
        verbose_name_plural = "Still from the film"


class RatingStar(models.Model):
    """RatingStars"""
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Stars"
        ordering = ["-value"]


class Rating(models.Model):
    """Rating of the film"""
    ip = models.CharField("User's IP", max_length=20)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="star")
    movie = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="film")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Reviews(models.Model):
    """Reviews of the film"""
    email = models.EmailField()
    name = models.CharField("name", max_length=50)
    text = models.TextField("Comment", max_length=3000)
    parent = models.ForeignKey('self', verbose_name="parent", on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="Film")

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


from django import template
from movies.models import Category, Film


register = template.Library()


@register.simple_tag()
def get_categories():
    """Output of all categories"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_film(count=5):
    """Recent Movies Added"""
    movies = Film.objects.order_by("id")[:count]
    return {"last_movies": movies}

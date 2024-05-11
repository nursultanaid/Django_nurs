from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField()
    duration = models.CharField(max_length=100)
    director = models.ForeignKey(Director,
                                 on_delete=models.CASCADE,
                                 related_name='movies',
                                 null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.created_at}'

STARS = ((star, '☆' * star)for star in range(1, 6))

class Review(models.Model):
    stars = models.IntegerField(default=1, choices=STARS)
    text = models.TextField()
    movie = models.ForeignKey(Movie,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

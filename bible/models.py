from django.db import models
from django.db.models import JSONField
import json

class Book(models.Model):
    name = models.CharField(max_length=100)
    testament = models.CharField(max_length=20)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.book.name} Chapter {self.number}"

class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="verses")
    number = models.PositiveIntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.chapter.book.name} {self.chapter.number}:{self.number}"

class VerseVector(models.Model):
    verse = models.OneToOneField(Verse, on_delete=models.CASCADE, related_name="vector")
    vector = models.TextField()  # JSON string of embedding list

    def set_vector(self, vector_array):
        self.vector = json.dumps(vector_array.tolist())  # convert numpy array to list, then to JSON string

    def get_vector(self):
        return json.loads(self.vector)


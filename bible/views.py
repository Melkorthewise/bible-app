from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter, Verse

def book_list(request):
    books = Book.objects.order_by('order')
    return render(request, 'bible/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    chapters = book.chapters.order_by('number')
    return render(request, 'bible/book_detail.html', {'book': book, 'chapters': chapters})

def chapter_detail(request, book_id, chapter_number):
    chapter = get_object_or_404(Chapter, book_id=book_id, number=chapter_number)
    verses = chapter.verses.order_by('number')
    return render(request, 'bible/chapter_detail.html', {'chapter': chapter, 'verses': verses})


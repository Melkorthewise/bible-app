import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from bible.models import Book, Chapter, Verse

class Command(BaseCommand):
    help = "Import Bible data from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_path",
            type=str,
            help="The path to the Bible JSON file to import",
        )

    def handle(self, *args, **options):
        json_path = options["json_path"]

        try:
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f"File '{json_path}' does not exist.")
        except json.JSONDecodeError as e:
            raise CommandError(f"Invalid JSON file: {e}")

        self.stdout.write(f"Starting import from {json_path}...")

        book_order = 1
        with transaction.atomic():
            for book_data in data["books"]:
                book_name = book_data["name"]
                testament = book_data.get("testament", "Unknown")

                book, created = Book.objects.get_or_create(
                    name=book_name,
                    defaults={
                        "order": book_order,
                        "testament": testament,
                    }
                )
                if created:
                    book_order += 1

                self.stdout.write(f"Importing Book: {book_name}")

                for chapter_data in book_data.get("chapters", []):
                    chapter_number = chapter_data.get("chapter")
                    if not isinstance(chapter_number, int):
                        self.stdout.write(self.style.WARNING(f"Skipping invalid chapter number: {chapter_number}"))
                        continue

                    chapter, _ = Chapter.objects.get_or_create(book=book, number=chapter_number)

                    for verse_data in chapter_data.get("verses", []):
                        verse_number = verse_data.get("verse")
                        verse_text = verse_data.get("text", "")

                        if not isinstance(verse_number, int):
                            self.stdout.write(self.style.WARNING(f"Skipping invalid verse number: {verse_number}"))
                            continue

                        Verse.objects.get_or_create(
                            chapter=chapter,
                            number=verse_number,
                            defaults={"text": verse_text},
                        )

        self.stdout.write(self.style.SUCCESS("Bible import complete!"))


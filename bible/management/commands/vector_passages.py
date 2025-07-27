from django.core.management.base import BaseCommand
from bible.models import Verse
from sentence_transformers import SentenceTransformer
from vectorstore.numpy_store import NumPyVectorStore
import os

class Command(BaseCommand):
    help = "Generate vector embeddings for all verses"

    def handle(self, *args, **options):
        vector_store = NumPyVectorStore()
        model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

        verses = Verse.objects.all()
        passages = [verse.text for verse in verses]

        embeddings = model.encode(passages)

        for verse, embedding in zip(verses, embeddings):
            metadata = {
                "verse_id": verse.id,
                "reference": f"{verse.chapter.book.name} {verse.chapter.number}:{verse.number}",
                "verse": verse.text
            }
            vector_store.add_vector(metadata["reference"], embedding, metadata)
            self.stdout.write(f"Processed verse {metadata['reference']}")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(base_dir, "../../../vectorstore/vectorstore.pkl")
        vector_store.save(save_path)

        self.stdout.write(self.style.SUCCESS("Vector generation and saving complete!"))


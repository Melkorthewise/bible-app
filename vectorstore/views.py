# vectorstore/views.py (or wherever you handle search)
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from sentence_transformers import SentenceTransformer
from vectorstore.factory import get_vector_store
import traceback

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
vector_store = get_vector_store()

def search_view(request):
    try:
        query = request.GET.get("q", "")
        if not query:
            return JsonResponse({"error": "No query provided"}, status=400)

        query_vector = model.encode([query])[0]
        results = vector_store.find_similar_vectors(query_vector, num_results=10)

        return JsonResponse({
            "query": query,
            "results": [
                {
                    "reference": meta["reference"],
                    "score": float(similarity),  # convert numpy.float32 to native float
                    "source": meta["verse"]
                }
                for _, similarity, meta in results
            ]
        })

    except Exception as e:
        traceback.print_exc()  # <-- this will print the error in the terminal
        return JsonResponse({"error": str(e)}, status=500)

from .forms import NameForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            query_vector = model.encode([form.cleaned_data])[0]
            results = vector_store.find_similar_vectors(query_vector, num_results=10)

            results = {
                "results": [
                {
                    "reference": meta["reference"],
                    "score": float(similarity),  # convert numpy.float32 to native float
                    "source": meta["verse"]
                }
                for _, similarity, meta in results
            ]
            }

            return render(request, "vectorstore/name.html", {"form": form, "query": form.cleaned_data["your_name"], "results": results})

            # return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "vectorstore/name.html", {"form": form})

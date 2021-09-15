from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def query(request, word):
    return render(request, "encyclopedia/query.html", {
        "querySearch": util.get_entry(word),
        "word": word
    })
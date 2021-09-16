from django.shortcuts import render, redirect
from django import forms

from . import util

class NewForm(forms.Form):
    newForm = forms.CharField(initial="Search Encyclopedia")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewForm()
    })

def query(request, word):
    return render(request, "encyclopedia/query.html", { 
        "querySearch": util.get_entry(word),
        "word": word,
        "form": NewForm()
    })

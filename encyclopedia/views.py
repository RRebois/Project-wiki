from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

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

def search(request):
    if request.method == "POST":
        # get the input 'q' from the user from the form in layout.html
        word = request.POST.get('q')

        # convert the word into lower case
        compare_word = word.lower()

        # Creates 2 variables:
        Entries = util.list_entries() # that will remain capitalized...
        entries = util.list_entries() # and this that will be converted to lowercase to be compared to 'word'
        
        for i in range(len(entries)):
            entries[i] = entries[i].lower()

        # Creates an empty dictionary called capitalize to associated the capitalized word associated to its lowercase version
        capitalize = {}
        for x in range(len(entries)):
            capitalize[Entries[x]] = entries[x]
        
        # use as a check
        # print(f"{capitalize}")

        return render(request, "encyclopedia/search.html", {
            "querySearch": util.get_entry(word),
            "word": word,
            "compare_word": compare_word,
            "capitalize": capitalize
        })
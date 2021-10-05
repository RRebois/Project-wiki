from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import random, secrets

from . import util

import markdown2

class NewPageForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'title', 'class': 'sizeform'}))
    content = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder': 'Your description here...'}))

# Creates a function that creates some variables of use along the doc:

def function():
    Entries = util.list_entries() # that will remain has it has been saved...
    entries = util.list_entries() # and this that will be converted to lowercase to be compared to 'word'
    random = secrets.choice(Entries)

    for i in range(len(entries)):
        entries[i] = entries[i].lower()

    # Creates an empty dictionary called capitalize to associated the capitalized word associated to its lowercase version
    capitalize = {}
    for x in range(len(entries)):
        capitalize[Entries[x]] = entries[x]
    
    return [Entries, entries, random, capitalize]

def index(request):
    values = function()
    #print(f"{values[0]}")
    #print(f"{values[2]}")
    return render(request, "encyclopedia/index.html", {
        "entries": values[0],
        "random": values[2]
    })

def query(request, word):
    values = function()
    compare_word = word.lower()
    
    if compare_word in values[1]:
        j = values[1].index(compare_word)
        word = values[0][j]
        #print(f"{word}")
        querySearch = markdown2.markdown(util.get_entry(word))
    else:
        querySearch = None

    return render(request, "encyclopedia/query.html", { 
        "querySearch": querySearch,
        "word": word, # word is capitalized
        "capitalize": values[3],
        "random": values[2]
    })

def search(request):
    values = function()
    if request.method == "POST":
        # get the input 'q' from the user from the form in layout.html
        word = request.POST.get('q')

        if word == '':
            danger = 50
            return HttpResponseRedirect(reverse("encyclopedia:index"), {
                "message": messages.add_message(request, danger, 'Not a valid search.')
            })

        # convert the word into lower case
        compare_word = word.lower()
        
        # use as a check
        # print(f"{capitalize}")

        if compare_word in values[1]:
            j = values[1].index(compare_word)
            word = values[0][j]
            querySearch = markdown2.markdown(util.get_entry(word))
        else:
            querySearch = None

        return render(request, "encyclopedia/search.html", {
            "querySearch": querySearch,
            "Entries": values[0],
            "word": word, 
            "random": values[2],
            "compare_word": compare_word,
            "capitalize": values[3]
        })
    else:
        return redirect("encyclopedia:index")

def newPage(request):
    values = function()
    if request.method == "POST":
        title = request.POST.get('title')
        titleLower = title.lower()
        content = request.POST.get('content')

        danger = 50

        if titleLower in values[1]:
            return render(request, "encyclopedia/newPage.html", {
                "form": NewPageForm,
                "message": messages.add_message(request, danger, 'Error: an entry with the same name already exists. Cannot overrride data. Entry not saved.'),
                "random": values[2]
            })

        else:
            util.save_entry(title,content)
            messages.add_message(request, messages.SUCCESS, 'Entry successfully saved. Thank you for your contribution!!')
            return HttpResponseRedirect(reverse("encyclopedia:query", args=(title,))) 
            # use HttpResponseRedirect instead of redirect to also redirect the flash message.
            # args=(title,) allows to pass the title parameter to the query view to open the new page correctly

    return render(request, "encyclopedia/newPage.html", {
        "form": NewPageForm,
        "random": values[2]
    })

def editPage(request):
    values = function()
    if request.method == "POST":
        title = request.POST.get('word')
        content = util.get_entry(title)

        #print(f"title sent is:{title}")
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "content": content,
            "random": values[2]
        })

def saveEdit(request):
    if request.method == "POST":

        title = request.POST.get('title')
        content = request.POST.get('content')

        util.save_entry(title,content)
        messages.add_message(request, messages.SUCCESS, 'Entry successfully saved. Thank you for your contribution!!')
        return HttpResponseRedirect(reverse("encyclopedia:query", args=(title,))) 
        # use HttpResponseRedirect instead of redirect to also redirect the flash message.
        # args=(title,) allows to pass the title parameter to the query view to open the new page correctly

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

def index(request):
    entries = util.list_entries()
    random = secrets.choice(entries)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random": random
    })

def query(request, word):
    Entries = util.list_entries() # that will remain has it has been saved...
    random = secrets.choice(Entries)

    compare_word = word.lower()
    #print(f"{compare_word}")
    entries = util.list_entries() # will be converted to lowercase to be compared to 'word'

    for i in range(len(entries)):
        entries[i] = entries[i].lower()

    # Creates an empty dictionary called capitalize to associated the capitalized word associated to its lowercase version
        capitalize = {}
        for x in range(len(entries)):
            capitalize[Entries[x]] = entries[x]

    
    if compare_word in entries:
        j = entries.index(compare_word)
        word = Entries[j]
        print(f"{word}")
        querySearch = markdown2.markdown(util.get_entry(word))
    else:
        querySearch = None

    return render(request, "encyclopedia/query.html", { 
        "querySearch": querySearch,
        "word": word, # word is capitalized
        "capitalize": capitalize,
        "random": random
    })

def search(request):
    if request.method == "POST":
        # get the input 'q' from the user from the form in layout.html
        word = request.POST.get('q')

        if word == '':
            danger = 50
            return HttpResponseRedirect(reverse("encyclopedia:index"), {
                "message": messages.add_message(request, danger, 'Not a valid search. Try again with a valid word')
            })

        # convert the word into lower case
        compare_word = word.lower()

        # Creates 2 variables:
        Entries = util.list_entries() # that will remain has it has been saved...
        entries = util.list_entries() # and this that will be converted to lowercase to be compared to 'word'
        random = secrets.choice(entries)

        for i in range(len(entries)):
            entries[i] = entries[i].lower()

        # Creates an empty dictionary called capitalize to associated the capitalized word associated to its lowercase version
        capitalize = {}
        for x in range(len(entries)):
            capitalize[Entries[x]] = entries[x]
        
        # use as a check
        # print(f"{capitalize}")

        if compare_word in entries:
            j = entries.index(compare_word)
            word = Entries[j]
            querySearch = markdown2.markdown(util.get_entry(word))
        else:
            querySearch = None

        return render(request, "encyclopedia/search.html", {
            "querySearch": querySearch,
            "Entries": Entries,
            "word": word, 
            "random": random,
            "compare_word": compare_word,
            "capitalize": capitalize
        })
    else:
        return redirect("encyclopedia:index")

def newPage(request):
    if request.method == "POST":
        title = request.POST.get('title').capitalize()
        content = request.POST.get('content')

        danger = 50
        compareTitles = util.list_entries()
        random = secrets.choice(compareTitles)

        if title in compareTitles:
            return render(request, "encyclopedia/newPage.html", {
                "form": NewPageForm,
                "message": messages.add_message(request, danger, 'Error: an entry with the same name already exists. Cannot overrride data. Entry not saved.'),
                "random": random
            })

        else:
            util.save_entry(title,content)
            messages.add_message(request, messages.SUCCESS, 'Entry successfully saved. Thank you for your contribution!!')
            return HttpResponseRedirect(reverse("encyclopedia:query", args=(title,))) 
            # use HttpResponseRedirect instead of redirect to also redirect the flash message.
            # args=(title,) allows to pass the title parameter to the query view to open the new page correctly

    entries = util.list_entries()
    random = secrets.choice(entries)
    return render(request, "encyclopedia/newPage.html", {
        "form": NewPageForm,
        "random": random
    })

def editPage(request):
    if request.method == "POST":
        title = request.POST.get('word')
        content = util.get_entry(title)
        entries = util.list_entries()
        random = secrets.choice(entries)

        #print(f"title sent is:{title}")
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "content": content,
            "random": random
        })

def saveEdit(request):
    if request.method == "POST":

        title = request.POST.get('title')
        content = request.POST.get('content')
        #if title.is_valid() == False or content.is_valid() == False:
         #   return render(request)
        #print(f"title={title}, content={content}")

        util.save_entry(title,content)
        messages.add_message(request, messages.SUCCESS, 'Entry successfully saved. Thank you for your contribution!!')
        return HttpResponseRedirect(reverse("encyclopedia:query", args=(title,))) 
        # use HttpResponseRedirect instead of redirect to also redirect the flash message.
        # args=(title,) allows to pass the title parameter to the query view to open the new page correctly

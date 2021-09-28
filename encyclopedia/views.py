from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from . import util

import markdown2
markdown2.markdown("*boo!*")  # or use `html = markdown_path(PATH)`
u'<p><em>boo!</em></p>\n'

from markdown2 import Markdown
markdowner = Markdown()
markdowner.convert("*boo!*")
u'<p><em>boo!</em></p>\n'
markdowner.convert("**boom!**")
u'<p><strong>boom!</strong></p>\n'


class NewPageForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'title', 'class': 'sizeform'}))
    content = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder': 'Your description here...'}))


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
    else:
        return redirect("encyclopedia:index")

def newPage(request):
    if request.method == "POST":
        title = request.POST.get('title').capitalize()
        content = request.POST.get('content')
        print(f"{title}, {content}")

        danger = 50
        compareTitles = util.list_entries()

        if title in compareTitles:
            return render(request, "encyclopedia/newPage.html", {
                "form": NewPageForm,
                "message": messages.add_message(request, danger, 'Error: an entry with the same name already exists. Cannot overrride data. Entry not saved.')
            })

        else:
            util.save_entry(title,content)
            messages.add_message(request, messages.SUCCESS, 'Entry successfully saved. Thank you for your contribution!!')
            return HttpResponseRedirect(reverse("encyclopedia:query", args=(title,))) 
            # use HttpResponseRedirect instead of redirect to also redirect the flash message.
            # args=(title,) allows to pass the title parameter to the query view to open the new page correctly

    return render(request, "encyclopedia/newPage.html", {
        "form": NewPageForm
    })
        
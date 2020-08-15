from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from . import util
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from random import randint, seed


markdowner = Markdown()

class New_entry(forms.Form):
    title = forms.CharField(label="Title")
    entry = forms.CharField(label="Entry")
    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    q = request.GET["q"]
    q = q.capitalize()
    entries = util.list_entries()
    context = util.get_entry(q)

    if context != None:
        return render(request, "encyclopedia/entry.html", {
            "title": q,
            "entries": context
        })
    else:
        for entry in entries:
            entry = entry.capitalize()
            if entry.startswith(q):
                context = []
                context.append(entry)

                if len(context) > 0:
                    return render(request, "encyclopedia/search.html", {
                        "title": "search page",
                        "entries": context
                    })

    return render(request, "encyclopedia/search.html", {
        "title": "Search not found",
        "m": "is 0 but here is a list of what we have!",
        "entries": entries
    })

def new(request):
    if request.method == "POST":
        form = New_entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]

            if util.get_entry(title) == None:
                util.save_entry(title, entry)
                return HttpResponseRedirect(reverse("dynamic", args=(title,)))
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "Entry exist!!!"
                })

    return render(request, "encyclopedia/new.html", {
        "form": New_entry()
    })

def edit(request, name):
    context = util.get_entry(name)

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("dynamic", args=(title,)))

    return render(request, "encyclopedia/edit.html", {
        "title": name,
        "entry": context
    })

def random(request):
    seed()
    entries = util.list_entries()
    count = len(entries)
    rand = randint(0, count-1)
    entry = entries[rand]
    return HttpResponseRedirect(reverse("dynamic", args=(entry,)))

def dynamic(request, name):
    context = util.get_entry(name)

    if context == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Not found!"
        })


    return render(request, "encyclopedia/entry.html", {
        "title": name,
        "entries": markdowner.convert(context)
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EventForm

from django.core.paginator import Paginator
from django.db.models import Q

from .models import Event, Category, City

def event_list(request):
    q = (request.GET.get("q") or "").strip()
    category_id = request.GET.get("category") or ""
    city_id = request.GET.get("city") or ""

    events = Event.objects.all().order_by("-id")


    if q:
        events = events.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(category__name__icontains=q) |
            Q(city__name__icontains=q)
        )


    if category_id:
        events = events.filter(category_id=category_id)

    if city_id:
        events = events.filter(city_id=city_id)


    categories = Category.objects.all().order_by("name")
    cities = City.objects.all().order_by("name")


    paginator = Paginator(events, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "events": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "cities": cities,
        "q": q,
        "selected_category": category_id,
        "selected_city": city_id,
    }
    return render(request, "events/list.html", context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "events/detail.html", {"event": event})

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "events/create.html", {"form": form})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.owner.id != request.user.id:
        return redirect("event_detail", pk=pk)

    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect("event_detail", pk=pk)

    return render(request, "events/edit.html", {"form": form, "event": event})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.owner.id != request.user.id:
        return redirect("event_detail", pk=pk)

    if request.method == "POST":
        event.delete()
        return redirect("event_list")

    return render(request, "events/delete.html", {"event": event})

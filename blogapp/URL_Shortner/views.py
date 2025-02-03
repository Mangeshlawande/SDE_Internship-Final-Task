# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import LongToShort, ClickAnalytics
from collections import defaultdict
import json
import requests

def hello_world(request):
    return HttpResponse("Hello World!!")

def home_page(request):
    context = {
        "submitted": False,
        "error": False,
    }

    if request.method == "POST":
        data = request.POST
        long_url = data['longurl']
        custom_name = data["custom_name"]

        try:
            # Create a new entry in the LongToShort model
            obj = LongToShort(long_url=long_url, short_url=custom_name)
            obj.save()

            # Set up context with newly created data
            context["submitted"] = True
            context["long_url"] = long_url
            context["short_url"] = request.build_absolute_uri() + custom_name
            context["date"] = obj.date
            context["clicks"] = obj.clicks
        except:
            context["error"] = True

    return render(request, "index.html", context)


def get_client_info(request):
    """Detect country and device type of a visitor."""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    ip = request.META.get('REMOTE_ADDR', '')

    country = "Unknown"
    try:
        # Use ipinfo.io API to get country based on the IP address
        response = requests.get(f"https://ipinfo.io/{ip}/json").json()
        country = response.get("country", "Unknown")
    except:
        pass

    # Detect device type
    if "mobile" in user_agent:
        device_type = "Mobile"
    else:
        device_type = "Desktop"

    return country, device_type


def redirect_url(request, short_url):
    """Redirect the user and log analytics."""
    obj = get_object_or_404(LongToShort, short_url=short_url)

    # Increment total click count for this URL
    obj.clicks += 1
    obj.save()

    # Get the client's country and device type
    country, device_type = get_client_info(request)

    # Update ClickAnalytics with the new click for this URL
    click, created = ClickAnalytics.objects.get_or_create(
        short_url=obj,
        country=country,
        device_type=device_type
    )
    if not created:
        click.click_count += 1
        click.save()

    # Redirect to the long URL
    return redirect(obj.long_url)


def all_analytics(request):
    """Display analytics for all URLs."""
    rows = LongToShort.objects.all()

    # Initialize counters for country and device clicks
    country_clicks = defaultdict(int)
    device_clicks = {"Desktop": 0, "Mobile": 0}

    # Get clicks grouped by country and device type
    analytics = ClickAnalytics.objects.all()
    for entry in analytics:
        country_clicks[entry.country] += entry.click_count
        device_clicks[entry.device_type] += entry.click_count

    # Prepare context data for rendering
    context = {
        "rows": rows,
        "countries": json.dumps(list(country_clicks.keys())),  # Country names for JS
        "clicks": json.dumps(list(country_clicks.values())),  # Click counts for JS
        "desktop": device_clicks["Desktop"],
        "mobile": device_clicks["Mobile"],
    }

    return render(request, "all_analytics.html", context)


def link_analytics(request, short_url):
    """Display analytics for a specific short URL."""
    obj = get_object_or_404(LongToShort, short_url=short_url)

    # Initialize counters for country and device clicks
    country_clicks = defaultdict(int)
    device_clicks = {"Desktop": 0, "Mobile": 0}

    # Get clicks grouped by country and device type for this URL
    analytics = ClickAnalytics.objects.filter(short_url=obj)
    for entry in analytics:
        country_clicks[entry.country] += entry.click_count
        device_clicks[entry.device_type] += entry.click_count

    # Prepare context data for rendering
    context = {
        "obj": obj,
        "countries": json.dumps(list(country_clicks.keys())),  # Country names for JS
        "clicks": json.dumps(list(country_clicks.values())),  # Click counts for JS
        "desktop": device_clicks["Desktop"],
        "mobile": device_clicks["Mobile"],
    }

    return render(request, "analytics.html", context)

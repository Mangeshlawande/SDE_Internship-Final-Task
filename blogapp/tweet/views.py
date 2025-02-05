from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm, TweetSearchForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
# Create your views here.

def index(request):
    # return HttpResponse(request, "welcome to tweets page ")
    return render(request, 'website/index.html', {})


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'website/tweet_list.html', {'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'website/tweet_form.html', {'form':form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'website/tweet_form.html', { 'form':form })


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect("tweet_list")
    return render(request, 'website/tweet_conform_delete.html', { 'tweet' : tweet })
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm  # Assuming you have this form defined

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            print(f"User {user.username} logged in successfully")
            # Debug the redirect process
            if request.user.is_authenticated:
                print(f"Redirecting {request.user.username} to tweet_list")
            else:
                print("Login failed, user not authenticated")
            return redirect('tweet_list')  # Ensure this URL name matches your 'urls.py'
        else:
            print("Form is invalid")
            print(form.errors)  # Print any form validation errors
            messages.error(request, 'There were some errors in the form. Please correct them and try again.')
    else:
        form = UserRegistrationForm()
        

    return render(request, 'registration/register.html', {'form': form})




def tweet_search(request):
    form = TweetSearchForm(request.GET or None)
    tweets = None

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            # Use Django ORM to filter tweets containing the search query
            tweets = Tweet.objects.filter(text__icontains=query)

    return render(request, 'website/tweet_search.html', {'form': form, 'tweets': tweets})
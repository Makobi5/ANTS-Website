from django.shortcuts import render, get_object_or_404,redirect
from .models import NewsArticle
from .models import NewsArticle, Event # <--- Import Event
from django.utils import timezone # <--- Import timezone
from django.db.models import Count
from django.db.models import Q
from django.contrib import messages
from .models import Subscriber # Import the new model
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Subscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags 
def news_list(request):
    # Get all news, newest first
    articles = NewsArticle.objects.all().order_by('-date_posted')
    return render(request, 'news/news_list.html', {'articles': articles})

def news_detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    
    # Get recent articles for the sidebar
    recent_articles = NewsArticle.objects.exclude(pk=pk).order_by('-date_posted')[:3]

    # NEW: Get "Related Gallery Albums" (Articles with photos)
    # We filter for articles that have EITHER a main image OR gallery images
    related_albums = NewsArticle.objects.annotate(
        photo_count=Count('gallery_images')
    ).filter(
        Q(image__isnull=False) | Q(photo_count__gt=0)
    ).exclude(pk=pk).order_by('-date_posted')[:3] # Show 3 recent albums
    
    context = {
        'article': article,
        'recent_articles': recent_articles,
        'related_albums': related_albums, # <--- Pass this to template
    }
    return render(request, 'news/news_detail.html', context)

def events_list(request):
    today = timezone.now().date()
    
    # Events happening today or in the future
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date', 'time')
    
    # Events that already happened
    past_events = Event.objects.filter(date__lt=today).order_by('-date', '-time')
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    }
    return render(request, 'news/events_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'news/event_detail.html', {'event': event})

def gallery(request):
    # 1. Get Articles that have at least one photo (Featured OR Gallery)
    # 2. Annotate them with the count of gallery images
    albums = NewsArticle.objects.annotate(
        photo_count=Count('gallery_images')
    ).filter(
        Q(image__isnull=False) | Q(photo_count__gt=0)
    ).order_by('-date_posted')

    # Pagination: You can limit this in the template or use Paginator later
    # For now, let's just send all of them, but the template will limit the view.
    
    return render(request, 'news/gallery.html', {'albums': albums})

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            if Subscriber.objects.filter(email=email).exists():
                messages.warning(request, "You are already subscribed!", extra_tags='newsletter')
            else:
                Subscriber.objects.create(email=email)
                
                # --- NEW EMAIL LOGIC ---
                subject = "Welcome to All Nations Theological College!"
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [email]

                # 1. Render the HTML template with data
                html_content = render_to_string('emails/welcome_email.html', {'email': email})
                
                # 2. Create a plain text version (for old email clients)
                text_content = strip_tags(html_content)

                # 3. Construct the email
                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                
                # 4. Send
                try:
                    msg.send()
                except Exception as e:
                    print(f"Error sending email: {e}")

                # Success Message
                success_msg = "Success! An email was just sent to confirm your subscription. Please check your inbox."
                messages.success(request, success_msg, extra_tags='newsletter')
        # Get the page the user came from
        next_url = request.META.get('HTTP_REFERER', '/')
        
        # Clean up existing anchors if any (prevents #newsletter#newsletter)
        if '#' in next_url:
            next_url = next_url.split('#')[0]
        return redirect(f"{next_url}#newsletter")
    
    return redirect('home')
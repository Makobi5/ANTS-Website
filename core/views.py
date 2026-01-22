from django.shortcuts import render
# Make sure to import the new models
from django.utils import timezone
from .models import Policy, DailySchedule
from django.db.models import Case, When, Value, IntegerField
from .models import Policy, DailySchedule, PageBanner, SliderImage
from news.models import NewsArticle, Event # Import the News model
from django.db.models import Q # Needed for advanced queries
from staff.models import StaffMember  # <--- New Import
from academics.models import Program  # <--- New Import
from .models import Policy 
from itertools import chain
from staff.models import StaffMember 

def home(request):
    # 1. Slider (Manual + News)
    manual_slides = SliderImage.objects.all().order_by('-created_at')
    news_slides = NewsArticle.objects.exclude(image='').order_by('-date_posted')[:5]
    combined_slides = list(chain(manual_slides, news_slides))
    
    # 2. News Grid
    latest_news_list = NewsArticle.objects.all().order_by('-date_posted')[:5]
    featured_news = latest_news_list[0] if latest_news_list else None
    other_news = latest_news_list[1:] if len(latest_news_list) > 1 else []

    # 3. Upcoming Events
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:3]

    # 4. FETCH THE PRINCIPAL (This was missing!)
    principal = StaffMember.objects.filter(category='PRINCIPAL').first()

    return render(request, 'core/home.html', {
        'combined_slides': combined_slides,
        'featured_news': featured_news,
        'other_news': other_news,
        'upcoming_events': upcoming_events,
        'principal': principal,  # Now this variable exists!
    })
def about(request):
    return render(request, 'core/about.html')

def who_we_are(request):
    # Fetch the banner specifically for the "Who We Are" page
    banner = PageBanner.objects.filter(page='WHO_WE_ARE').first()
    
    return render(request, 'core/who_we_are.html', {'banner': banner})

def statement_of_faith(request):
    return render(request, 'core/statement_of_faith.html')

def policies(request):
    return render(request, 'core/policies.html')

def daily_schedule(request):
    return render(request, 'core/schedule.html')

def policies(request):
    # Fetch all policies
    policies_list = Policy.objects.all().order_by('-uploaded_at')
    return render(request, 'core/policies.html', {'policies': policies_list})

def daily_schedule(request):
    # Define the exact order you want the days to appear
    schedule_items = DailySchedule.objects.annotate(
        day_rank=Case(
            When(day_category='MONDAY-FRIDAY', then=Value(1)),
            When(day_category='MONDAY', then=Value(2)),
            When(day_category='TUESDAY', then=Value(3)),
            When(day_category='WEDNESDAY', then=Value(4)),
            When(day_category='THURSDAY', then=Value(5)),
            When(day_category='FRIDAY', then=Value(6)),
            When(day_category='SATURDAY', then=Value(7)),
            When(day_category='SUNDAY', then=Value(8)),
            default=Value(100),
            output_field=IntegerField(),
        )
    ).order_by('day_rank', 'start_time')
    
    return render(request, 'core/schedule.html', {'items': schedule_items})


def global_search(request):
    query = request.GET.get('q')
    
    if query:
        # 1. Search News
        news_results = NewsArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        
        # 2. Search Events
        event_results = Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        # 3. Search Staff (This will find "Principal")
        staff_results = StaffMember.objects.filter(
            Q(name__icontains=query) | Q(role__icontains=query) | Q(bio__icontains=query)
        )

        # 4. Search Programs (Courses)
        program_results = Program.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        )

        # 5. Search Documents/Policies
        policy_results = Policy.objects.filter(
            Q(title__icontains=query)
        )

    else:
        news_results = event_results = staff_results = program_results = policy_results = []

    # Check if we found anything at all
    results_found = any([news_results, event_results, staff_results, program_results, policy_results])

    context = {
        'query': query,
        'results_found': results_found,
        'news_results': news_results,
        'event_results': event_results,
        'staff_results': staff_results,
        'program_results': program_results,
        'policy_results': policy_results,
    }

    return render(request, 'core/search_results.html', context)
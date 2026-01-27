from django.shortcuts import render, get_object_or_404,redirect
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
from .models import SliderImage, PageBanner, Partner, Testimonial 
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages
from .models import ContactDepartment
from django.urls import reverse

def home(request):
    # --- 1. HERO SLIDER LOGIC ---
    # Fetch Manual Slides (Created in Admin)
    manual_slides = SliderImage.objects.all().order_by('-created_at')
    # Fetch Latest News for Slider (Only those with images)
    news_slides = NewsArticle.objects.exclude(image='').order_by('-date_posted')[:5]
    # Combine them into one list for the template
    combined_slides = list(chain(manual_slides, news_slides))
    
    # --- 2. OFFICE OF THE PRINCIPAL ---
    # Fetch the staff member marked as 'PRINCIPAL'
    principal = StaffMember.objects.filter(category='PRINCIPAL').first()

    # --- 3. UNIVERSITY NEWS GRID ---
    # Fetch latest 5 articles
    latest_news_list = NewsArticle.objects.all().order_by('-date_posted')[:5]
    # Split them: First one is "Featured" (Big), the rest are "Other" (Small)
    featured_news = latest_news_list[0] if latest_news_list else None
    other_news = latest_news_list[1:] if len(latest_news_list) > 1 else []

    # --- 4. UPCOMING EVENTS (Parallax Section) ---
    today = timezone.now().date()
    # Fetch events happening today or in the future, limit to 3 for the row
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:3]

    # --- 5. TESTIMONIALS ---
    # Fetch latest 3 testimonials for the "Voices of ANTS" section
    testimonials = Testimonial.objects.all().order_by('-created_at')[:3]

    # --- 6. PARTNERS ---
    # Fetch all partners
    partners = Partner.objects.all()

    # Pass everything to the template
    return render(request, 'core/home.html', {
        'combined_slides': combined_slides,
        'principal': principal,
        'featured_news': featured_news,
        'other_news': other_news,
        'upcoming_events': upcoming_events,
        'testimonials': testimonials,
        'partners': partners,
    })
    
# New View for the Notebook Page
def testimonial_detail(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    # Get other testimonials for the sidebar
    others = Testimonial.objects.exclude(pk=pk)[:4]
    return render(request, 'core/testimonial_detail.html', {'testimonial': testimonial, 'others': others})    
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


def contact(request):
    departments = ContactDepartment.objects.prefetch_related('people').all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            full_message = f"Message from: {name} ({email})\n\n{message}"
            
            try:
                # 1. Send Email to info@ants.ac.ug
                send_mail(
                    f"Website Inquiry: {subject}",
                    full_message,
                    email, # From User
                    ['info@ants.ac.ug'], # To Official School Email
                    fail_silently=False
                )
                
                # 2. Success Message
                messages.success(request, "Thank you! Your message has been sent. We will contact you shortly.", extra_tags='contact_form')
                
                # 3. Redirect to the Anchor (Keeps user at the form, Clears the inputs)
                return redirect(reverse('contact') + '#contact-section')
                
            except Exception as e:
                print(f"Email Error: {e}") # Print error to terminal
                messages.error(request, "Something went wrong. Please try again later.", extra_tags='contact_form')
                
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {
        'form': form,
        'departments': departments
    })
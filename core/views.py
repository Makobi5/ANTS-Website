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
from .models import StudentLeader,PageBanner 
from .models import AlumniMember
from .forms import AlumniRegistrationForm
from news.models import NewsImage 
from .models import ServiceDepartment, Sermon, OutreachProgram,OutreachProgram
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from itertools import chain
from news.models import NewsArticle, Event
from staff.models import StaffMember
from .models import SliderImage, Partner, Testimonial
from .models import ChapelEvent
from .models import ChapelPreacher
from datetime import date, timedelta
from .models import Notice
from django.core.paginator import Paginator

# If you have already created the Outreach and Sermon models, ensure they are imported:
# from outreach.models import OutreachProgram 
# from chapel.models import Sermon

def home(request):
    today = timezone.now().date()

    # 1. Manual Slides
    manual_slides = list(SliderImage.objects.all().order_by('-created_at')[:3])
    for slide in manual_slides: slide.slide_type = 'manual'
    
    # 2. News Slides
    news_slides = list(NewsArticle.objects.filter(show_on_slider=True).exclude(image='').order_by('-date_posted')[:5])
    for slide in news_slides: slide.slide_type = 'news'
    
    # 3. Outreach Slides
    outreach_slides = list(OutreachProgram.objects.filter(
        show_on_slider=True
    ).exclude(image='').order_by('-id')[:3])
    for slide in outreach_slides: slide.slide_type = 'outreach'

    # 4. SERMON SLIDES (FIXED!)
    # Removed .exclude(image='') so it works with YouTube auto-thumbnails
    sermon_slides = list(Sermon.objects.filter(show_on_slider=True).order_by('-date_preached')[:2])
    for slide in sermon_slides: slide.slide_type = 'sermon'
    chapel_event_slides = list(ChapelEvent.objects.filter(
        show_on_slider=True, date__gte=today
    ).exclude(image='').exclude(image=None).order_by('date')[:2])
    for slide in chapel_event_slides: slide.slide_type = 'chapel_event'
    # 5. Upcoming Event Slides (Auto-expires correctly)
    event_slides = list(Event.objects.filter(show_on_slider=True, date__gte=today).exclude(image='').order_by('date')[:3])
    for slide in event_slides: slide.slide_type = 'event'

    

    # Combine ALL into the slider
    combined_slides = list(chain(manual_slides, news_slides, outreach_slides, sermon_slides, event_slides,chapel_event_slides ))
    
    # --- OFFICE OF THE PRINCIPAL ---
    principal = StaffMember.objects.filter(category='PRINCIPAL').first()

    # --- UNIVERSITY NEWS GRID ---
    latest_news_list = NewsArticle.objects.all().order_by('-date_posted')[:5]
    featured_news = latest_news_list[0] if latest_news_list else None
    other_news = latest_news_list[1:] if len(latest_news_list) > 1 else[]
    latest_notices = Notice.objects.filter(is_published=True).order_by('-is_pinned', '-date_posted')[:5]
    
    # --- UPCOMING EVENTS ---
        # --- UPCOMING EVENTS (Combined: Regular + Chapel Events) ---
    regular_events = list(Event.objects.filter(date__gte=today).order_by('date')[:3])
    for e in regular_events:
        e.event_type = 'regular'

    chapel_upcoming = list(ChapelEvent.objects.filter(date__gte=today).order_by('date')[:3])
    for e in chapel_upcoming:
        e.event_type = 'chapel'

    # Merge and sort by date, take the nearest 3
    upcoming_events = sorted(
        regular_events + chapel_upcoming,
        key=lambda x: x.date
    )[:3]

    # --- TESTIMONIALS & PARTNERS ---
    testimonials = Testimonial.objects.all().order_by('-created_at')[:3]
    partners = Partner.objects.all()

    return render(request, 'core/home.html', {
        'combined_slides': combined_slides,
        'principal': principal,
        'featured_news': featured_news,
        'other_news': other_news,
        'upcoming_events': upcoming_events,
        'latest_notices': latest_notices,
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

def notices_list(request):
    category = request.GET.get('category', 'all')
    notices = Notice.objects.filter(is_published=True)
    if category and category != 'all':
        notices = notices.filter(category=category)
    return render(request, 'notices/notices_list.html', {
        'notices': notices,
        'active_category': category,
        'categories': Notice.CATEGORY_CHOICES,
    })
 
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk, is_published=True)
    return render(request, 'notices/notice_detail.html', {'notice': notice})


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
    
    
def student_guild(request):
    # 1. Fetch the Group Photo Banner
    guild_banner = PageBanner.objects.filter(page='GUILD').first()

    # 2. Fetch Leaders
    all_leaders = StudentLeader.objects.all()
    current_cabinet = all_leaders.filter(cabinet_year='2026').order_by('order')
    past_leaders = all_leaders.exclude(cabinet_year='2026').order_by('-cabinet_year', 'order')
    
    return render(request, 'core/students/guild.html', {
        'guild_banner': guild_banner, # <--- Pass image to template
        'current_cabinet': current_cabinet,
        'past_leaders': past_leaders
    })

def alumni(request):
    # 1. Handle Form Submission
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # Saves with is_approved=False by default
            messages.success(request, "Registration successful! Your profile is pending approval by the admin.")
            return redirect('alumni') # Reload page to clear form
    else:
        form = AlumniRegistrationForm()

    # 2. Fetch ONLY Approved Alumni for display
    approved_alumni = AlumniMember.objects.filter(is_approved=True).order_by('-graduation_year')

    return render(request, 'core/students/alumni.html', {
        'approved_alumni': approved_alumni,
        'form': form
    })

def life_at_ants(request):
    return render(request, 'core/students/life.html')

def fees_structure(request):
    from .models import FeeStructure
    fees = FeeStructure.objects.all()
    return render(request, 'core/students/fees.html', {'fees': fees})   
def student_manual(request):
    # Fetch policies specifically titled "Student Manual" or category "Manual"
    # For now, let's just fetch ALL policies but show them on a dedicated page
    manuals = Policy.objects.filter(title__icontains="Manual") 
    return render(request, 'core/students/manual.html', {'manuals': manuals})

# 1. Sports & Athletics
def life_sports(request):
    # Fetch 3 random or latest images for the "Featured Gallery" section
    # We use 'order_by' to get recent ones
    gallery_preview = NewsImage.objects.all().order_by('-id')[:3]
    return render(request, 'core/students/life_sports.html', {'gallery': gallery_preview})

# 2. Accommodation / Housing
def life_housing(request):
    return render(request, 'core/students/life_housing.html')

# 3. Dining
def life_dining(request):
    return render(request, 'core/students/life_dining.html')

def service_detail(request, slug):
    service = get_object_or_404(ServiceDepartment, slug=slug)
    return render(request, 'core/services/service_detail.html', {'service': service})

def ants_chapel(request):
    # --- 1. SERMON LOGIC (PAGINATED) ---
    all_sermons = Sermon.objects.all().order_by('-date_preached')
    latest_sermon = all_sermons.first()

    # We paginate the sermons starting FROM the second one (index 1 onwards)
    # so we don't repeat the latest sermon which is shown in the big video player
    remaining_sermons = all_sermons[1:] if all_sermons.count() > 1 else Sermon.objects.none()

    paginator = Paginator(remaining_sermons, 5) # Load 5 per "chunk"
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # --- 2. WEEKLY PREACHER LOGIC (EXISTING) ---
    today = date.today()
    if today.weekday() == 6:  # Sunday
        monday = today + timedelta(days=1)
    else:
        monday = today - timedelta(days=today.weekday())

    DAY_ORDER = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sun': 5}
    chapel_preachers = sorted(
        ChapelPreacher.objects.filter(week_of=monday),
        key=lambda p: DAY_ORDER.get(p.day, 99)
    )

    # --- 3. EVENT LOGIC (EXISTING) ---
    featured_event = ChapelEvent.objects.filter(is_featured=True).order_by('date').first()
    chapel_events = ChapelEvent.objects.filter(
        is_featured=True,
        end_date__gte=timezone.now().date()
    ).order_by('date')[:8]

    context = {
        'latest_sermon': latest_sermon,
        'recent_sermons': page_obj, # This is now a Page object
        'has_next': page_obj.has_next(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'chapel_events': chapel_events,
        'featured_event': featured_event,
        'chapel_preachers': chapel_preachers,
    }

    # HTMX CHECK: If this is an AJAX "Load More" request, only return the partial HTML
    if request.headers.get('HX-Request'):
        return render(request, 'core/sermon_list_partial.html', context)

    return render(request, 'core/chapel.html', context)

def donations(request):
    """
    Donations page view
    """
    # You can add context data here if needed
    # For example, fetching donation statistics from database
    context = {
        'page_title': 'Support ANTS | Donations',
        # Add any dynamic data you want to pass to the template
    }
    return render(request, 'core/donations.html', context)

def community_outreach(request):
    programs = OutreachProgram.objects.all()
    return render(request, 'core/community_outreach.html', {'programs': programs})

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)
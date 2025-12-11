from django.shortcuts import render, get_object_or_404
from .models import Program

def program_list(request, category_slug):
    # Map the URL words to Database categories
    category_map = {
        'bachelors': 'BACHELOR',
        'diplomas': 'DIPLOMA',
        'certificates': 'CERTIFICATE',
        'short-courses': 'SHORT',
    }
    
    # 1. Get the database code (e.g., 'BACHELOR')
    db_category = category_map.get(category_slug)
    
    # 2. Fetch the programs that match
    programs = Program.objects.filter(category=db_category)
    
    # 3. Create a nice title for the page
    titles = {
        'bachelors': 'Bachelor Programs',
        'diplomas': 'Diploma Programs',
        'certificates': 'Certificate Programs',
        'short-courses': 'Short Courses',
    }
    page_title = titles.get(category_slug, 'Our Programs')

    context = {
        'programs': programs,
        'title': page_title
    }
    return render(request, 'academics/program_list.html', context)

def program_detail(request, slug):
    # Fetch the specific program using its unique slug
    program = get_object_or_404(Program, slug=slug)
    return render(request, 'academics/program_detail.html', {'program': program})
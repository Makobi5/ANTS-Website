from django import template
from academics.models import Program
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def get_featured_programs():
    # Returns all programs where the checkbox is ticked
    return Program.objects.filter(is_featured_in_menu=True).order_by('title')

@register.filter
def format_curriculum(value):
    if not value:
        return value

    # Format 1: YEAR/SEMESTER structure
    if re.search(r'YEAR\s+\w+\s+SEMESTER\s+\w+', value):
        sections = re.split(r'(YEAR\s+\w+\s+SEMESTER\s+\w+)', value)
        html = ''
        for section in sections:
            section = section.strip()
            if not section:
                continue
            if re.match(r'YEAR\s+\w+\s+SEMESTER\s+\w+', section):
                html += f'<h6 class="curriculum-semester-title">{section}</h6>'
            else:
                subjects = [s.strip() for s in section.split('•') if s.strip()]
                if subjects:
                    html += '<ul class="curriculum-list">'
                    for subject in subjects:
                        html += f'<li>{subject}</li>'
                    html += '</ul>'
        return mark_safe(html)

    # Format 2: Bullet point • separated
    elif '•' in value:
        subjects = [s.strip() for s in value.split('•') if s.strip()]
        html = '<ul class="curriculum-list">'
        for subject in subjects:
            html += f'<li>{subject}</li>'
        html += '</ul>'
        return mark_safe(html)

    # Format 3: Numbered list (admission requirements style)
    elif re.search(r'^\d+\.', value, re.MULTILINE):
        lines = [l.strip() for l in value.strip().splitlines() if l.strip()]
        html = ''
        in_list = False
        for line in lines:
            # Main numbered heading e.g. "1. Requirements for Direct Entry:"
            if re.match(r'^\d+\.', line):
                if in_list:
                    html += '</ul>'
                    in_list = False
                html += f'<h6 class="curriculum-semester-title">{line}</h6>'
                html += '<ul class="curriculum-list">'
                in_list = True
            # Sub-point e.g. "a) Five passes..." or "A. At least five..."
            elif re.match(r'^[a-zA-Z][.)]\s', line):
                html += f'<li>{line}</li>'
            # Plain continuation line
            else:
                html += f'<li>{line}</li>'
        if in_list:
            html += '</ul>'
        return mark_safe(html)

    # Format 4: Plain sentences — split into pills
    else:
        subjects = re.split(r'\. (?=[A-Z])', value.strip())
        html = '<ul class="curriculum-list">'
        for subject in subjects:
            subject = subject.strip().rstrip('.')
            if subject:
                html += f'<li>{subject}</li>'
        html += '</ul>'
        return mark_safe(html)
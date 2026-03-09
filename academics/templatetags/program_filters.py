from django import template
import re

register = template.Library()

@register.filter
def format_curriculum(value):
    if not value:
        return value
    
    # Split by YEAR pattern
    sections = re.split(r'(YEAR\s+\w+\s+SEMESTER\s+\w+)', value)
    
    html = ''
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
        
        if re.match(r'YEAR\s+\w+\s+SEMESTER\s+\w+', section):
            html += f'<h6 class="curriculum-semester-title">{section}</h6>'
        else:
            # Split by bullet point
            subjects = [s.strip() for s in section.split('•') if s.strip()]
            if subjects:
                html += '<ul class="curriculum-list">'
                for subject in subjects:
                    html += f'<li>{subject}</li>'
                html += '</ul>'
    
    return html
from django.contrib import admin
from .models import Policy, DailySchedule, PageBanner,SliderImage  # Import it here
from django.utils.html import mark_safe
from .models import  Partner, Testimonial # <--- Add imports
from .models import ContactDepartment, ContactPerson
from .models import StudentLeader
from .models import AlumniMember
from .models import ServiceDepartment, Sermon
from django.contrib import admin
from .models import DonationCategory, Donation, DonationTestimonial, DonationImpactStory, OutreachProgram, OutreachImage, Sermon
from staff.models import StaffMember
from .models import FeeStructure
from .models import ChapelEvent
from .models import ChapelPreacher
from .models import Notice


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

@admin.register(DailySchedule)
class DailyScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_category', 'period', 'start_time', 'activity', 'location')
    list_filter = ('day_category', 'period')
    list_editable = ('activity', 'location')
    
    # Modern Time Picker override
    from django.db import models
    from django import forms
    formfield_overrides = {
        models.TimeField: {'widget': forms.TimeInput(attrs={'type': 'time'})},
    }

@admin.register(PageBanner)
class PageBannerAdmin(admin.ModelAdmin):
    list_display = ('page', 'caption')

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    # Update list_display to show the preview first
    list_display = ('image_preview', 'title', 'created_at')
    
    # Enable clicking on the image to edit
    list_display_links = ('image_preview', 'title')

    # Create the function to render the image
    def image_preview(self, obj):
        if obj.image:
            # Renders a small 150px wide image
            return mark_safe(f'<img src="{obj.image.url}" width="150" style="border-radius:5px; border:1px solid #ccc;" />')
        return "No Image"
    
    image_preview.short_description = 'Slide Preview'   
    
    
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at') # Added created_at to see when it was added
    list_display_links = ('name',) # <--- This makes the name clickable for editing  
    
class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 1

@admin.register(ContactDepartment)
class ContactDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    inlines = [ContactPersonInline]  
    
@admin.register(StudentLeader)
class StudentLeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'cabinet_year', 'order')
    list_filter = ('cabinet_year',)
    list_editable = ('order',)     
def approve_alumni(modeladmin, request, queryset):
    queryset.update(is_approved=True)
approve_alumni.short_description = "Approve selected alumni for website Display"

@admin.register(AlumniMember)
class AlumniMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'graduation_year', 'program', 'is_approved')
    list_filter = ('is_approved', 'graduation_year')
    search_fields = ('full_name', 'email')
    actions = [approve_alumni] # Adds the action to the dropdown menu     
    
# 1. Create the Inline View for Staff
class StaffMemberInline(admin.TabularInline):
    model = StaffMember
    extra = 1 # Shows 1 empty row to add a new person
    fields = ('name', 'role', 'qualifications', 'photo', 'category') # Fields to edit directly
    fk_name = "service_department" # Explicitly tell Django which field links them

# 2. Update ServiceDepartmentAdmin to include the Inline
@admin.register(ServiceDepartment)
class ServiceDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_title')
    prepopulated_fields = {'slug': ('name',)}
    
    # This adds the Staff section inside the Department page
    inlines = [StaffMemberInline]   
    
    
# 3. Update Sermon Admin
@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date_preached', 'show_on_slider')
    list_editable = ('show_on_slider',)  
    

@admin.register(ChapelEvent)
class ChapelEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'end_date', 'is_featured', 'show_on_slider']
    list_editable = ['is_featured', 'show_on_slider']
    list_filter = ['is_featured', 'show_on_slider']
    ordering = ['date']    

@admin.register(ChapelPreacher)
class ChapelPreacherAdmin(admin.ModelAdmin):
    list_display = ('week_of', 'day', 'preacher_name', 'role', 'service_type')
    list_filter = ('week_of', 'service_type')
    ordering = ('-week_of', 'day')
        
@admin.register(DonationCategory)
class DonationCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'target_amount', 'is_active', 'order']
    list_filter = ['category_type', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'currency', 'category', 'payment_method', 
                   'status', 'date_received', 'receipt_issued']
    list_filter = ['status', 'payment_method', 'category', 'receipt_issued', 
                  'date_received', 'is_anonymous']
    search_fields = ['donor_name', 'donor_email', 'transaction_reference', 
                    'receipt_number', 'purpose']
    date_hierarchy = 'date_received'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('category', 'amount', 'currency', 'payment_method', 
                      'transaction_reference', 'purpose', 'donor_message')
        }),
        ('Status & Processing', {
            'fields': ('status', 'date_received', 'date_confirmed', 
                      'receipt_issued', 'receipt_number', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_receipt_issued']
    
    def mark_as_confirmed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='CONFIRMED', date_confirmed=timezone.now().date())
        self.message_user(request, f'{updated} donation(s) marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected donations as confirmed"
    
    def mark_receipt_issued(self, request, queryset):
        updated = queryset.update(receipt_issued=True)
        self.message_user(request, f'Receipt issued for {updated} donation(s).')
    mark_receipt_issued.short_description = "Mark receipts as issued"


@admin.register(DonationTestimonial)
class DonationTestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'is_featured', 'is_active', 'order']
    list_filter = ['is_featured', 'is_active']
    search_fields = ['name', 'quote', 'title']
    list_editable = ['is_featured', 'order']


@admin.register(DonationImpactStory)
class DonationImpactStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'beneficiary_name', 'is_published', 'publish_date']
    list_filter = ['is_published', 'category', 'publish_date']
    search_fields = ['title', 'summary', 'beneficiary_name']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    
    fieldsets = (
        ('Story Details', {
            'fields': ('title', 'slug', 'category', 'featured_image', 'summary', 'full_story')
        }),
        ('Beneficiary (Optional)', {
            'fields': ('beneficiary_name', 'beneficiary_photo'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'publish_date')
        }),
    )
# 1. Create Inline for Outreach Images
class OutreachImageInline(admin.TabularInline):
    model = OutreachImage
    extra = 5 # 5 slots for photos at once
        
# 2. Update Outreach Admin
@admin.register(OutreachProgram)
class OutreachProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'show_on_slider')
    list_editable = ('show_on_slider',) # Toggle from list
    inlines = [OutreachImageInline] # Add gallery here 




@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('program_name', 'tuition_per_semester', 'functional_fees', 'total', 'academic_year', 'order')
    list_editable = ('order', 'academic_year')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display   = ('title', 'category', 'target_audience', 'date_posted', 'is_published', 'is_pinned')
    list_filter    = ('category', 'target_audience', 'is_published', 'is_pinned')
    search_fields  = ('title', 'content')
    list_editable  = ('is_published', 'is_pinned')
    ordering       = ('-is_pinned', '-date_posted')
    date_hierarchy = 'date_posted'
    fieldsets = (
        ('Notice Details', {
            'fields': ('title', 'content', 'category', 'target_audience', 'attachment')
        }),
        ('Publishing', {
            'fields': ('date_posted', 'is_published', 'is_pinned')
        }),
    )    
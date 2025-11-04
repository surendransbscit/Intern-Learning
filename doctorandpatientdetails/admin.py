from django.contrib import admin
from .models import Patient,Student,Teachar, Hobby, Hospital , AdmittePatientDetails
from django_summernote.admin import SummernoteModelAdmin
import django.apps
from django_summernote.models import Attachment

class AgeRangeFilter(admin.SimpleListFilter):
    title = 'Age Range'    
    parameter_name = 'age_range'

    def lookups(self, request, model_admin):
        return [
            ('child', 'Below 16'),
            ('boys', '16-30'),
            ('mens', '31+'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'child':
            return queryset.filter(age__lt=16)
        if value == 'boys':
            return queryset.filter(age__gte=16, age__lte=30)
        if value == 'mens':
            return queryset.filter(age__gte=31)
        return queryset


class PatientAdmin(SummernoteModelAdmin):
    fields = ['name', 'age', 'doctor', 'diagnosis']
    list_display = ['name', 'age', 'doctor', 'diagnosis']
    list_filter = ['name', 'age', AgeRangeFilter]
    search_fields = ['name', 'diagnosis', 'doctor__name']
    summernote_fields = ('diagnosis',)

    

admin.site.index_title="Hospital Management System"
admin.site.site_header="Hospital Management"
admin.site.site_title ="Hospital Management"

admin.site.register(Patient, PatientAdmin)


class HospitalAdmin(SummernoteModelAdmin):
    # fields = ['name', 'address', 'is_activate', 'create_on']
    readonly_fields = ['create_on']
    summernote_fields = ('address',)
    list_display = ['name',  'is_activate']
    list_editable = ["is_activate"]
    list_per_page = 8
    search_fields = ['is_activate','name']
    list_filter = ['is_activate']
    fieldsets = [
        (
            "Main Details",
            {
                "classes": ["collapse"],
                "fields": ['name', 'address']
            },
        ),
        (
            "Default Details",
            {
                "classes": [ "collapse"],
                "fields": ['is_activate', 'create_on']
            }
        )
    ]

admin.site.register(Hospital, HospitalAdmin)


admin.site.unregister(Attachment)


class AdmittePatientDetailsAdmin(admin.ModelAdmin):
    fields = [ 'patient', 'hospital', 'is_activate']
    list_display = [ 'patient','hospital', 'is_activate']
    list_editable = ['is_activate']
    search_fields = ['patient__name','hospital__name']
    ordering = ['patient__name']

admin.site.register(AdmittePatientDetails, AdmittePatientDetailsAdmin)


class TeacharInline(admin.TabularInline):
    model = Student
    extra = 0

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name','age']
    inlines = [
        TeacharInline,
    ]

admin.site.register(Teachar, TeacherAdmin)

class HobbyAdmin(admin.ModelAdmin):
    list_display=['id','name']
    ordering = ["-id"]

admin.site.register(Hobby, HobbyAdmin)


class StudentAdmin(admin.ModelAdmin):
    fields = ['name','age','teachar','habbice']
    list_editable = ['age']
    list_display = ['name','age','teachar']
    raw_id_fields = ['teachar', 'habbice']
    list_per_page = 5

admin.site.register(Student, StudentAdmin)















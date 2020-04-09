from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (CustomUser, SchoolData, SchoolType, State, StudentData,
                     Subject, TutorData)

admin.site.register(SchoolData)
admin.site.register(SchoolType)
admin.site.register(State)
admin.site.register(Subject)


class StudentDataInline(admin.StackedInline):
    model = StudentData
    verbose_name = "Schülerdaten"
    verbose_name_plural = verbose_name


class TutorDataInline(admin.StackedInline):
    model = TutorData
    verbose_name = "Tutordaten"
    verbose_name_plural = verbose_name
    fields = ['schooldata', 'subjects', 'verified',
              'verification_file', 'profile_picture', 'image_tag']
    readonly_fields = ['image_tag']


class TutorDataFilter(admin.SimpleListFilter):
    title = _('Tutor')

    parameter_name = 'is_tutor'

    def lookups(self, request, model_admin):
        return (('not_null', _('Yes')),
                ('null', _('No')))

    def queryset(self, request, queryset):
        if self.value() == 'null':
            return queryset.filter(tutordata__isnull=True)
        elif self.value() == 'not_null':
            return queryset.filter(tutordata__isnull=False)


class StudentDataFilter(admin.SimpleListFilter):
    title = _('Schüler')

    parameter_name = 'is_student'

    def lookups(self, request, model_admin):
        return (('not_null', _('Yes')),
                ('null', _('No')))
    def queryset(self, request, queryset):
        if self.value() == 'null':
            return queryset.filter(studentdata__isnull=True)
        elif self.value() == 'not_null':
            return queryset.filter(studentdata__isnull=False)


class UnverifiedTutorFilter(admin.SimpleListFilter):
    title = _('Ist verifizierter Tutor')

    parameter_name = 'verified_tutor'

    def lookups(self, request, model_admin):
        return (('yes', _('Unverified')),
                ('no', _('Verified')))

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(tutordata__isnull=False).filter(tutordata__verified=False)
        elif self.value() == 'no':
            return queryset.filter(tutordata__isnull=False).filter(tutordata__verified=True)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = [
        StudentDataInline,
        TutorDataInline
    ]
    list_display = ('email', 'first_name', 'last_name',
                    'state', 'is_staff', 'is_active', 'is_tutor', 'is_student', 'email_verified')
    list_filter = ('is_staff', 'is_active', 'email_verified', UnverifiedTutorFilter, StudentDataFilter, TutorDataFilter, 'state'
                   )
    fieldsets = (
        (None, {'fields':
                ('email', 'email_verified', 'first_name', 'last_name', 'gender', 'state', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',), 'fields': (
                'email', 'first_name', 'state', 'password1', 'password2',
                    'is_staff', 'is_active')}), )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)

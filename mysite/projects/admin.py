from django.contrib import admin
from projects.models import Project


# Register your models here.
def approve(modeladmin, request, queryset):
    queryset.update(is_approved=True)


def deny(modeladmin, request, queryset):
    queryset.update(is_approved=False)


approve.short_description = "Approve Projects"
deny.short_description = "Disapprove Projects"


class ProjectAdmin(admin.ModelAdmin):
    actions = [approve, deny]


admin.site.register(Project, ProjectAdmin)

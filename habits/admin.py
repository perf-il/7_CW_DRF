from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'time', 'action', 'is_enjoyable', 'related_habit','periodicity',
                    'reward', 'execution_time', 'is_public', )

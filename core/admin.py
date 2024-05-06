from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Session, Term, NewsAndEvents


admin.site.register(Term)
admin.site.register(Session)
admin.site.register(NewsAndEvents)

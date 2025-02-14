# events/views.py
from django.views.generic import ListView, DetailView
from .models import Event, EventCategory
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import datetime

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True)

        # Category Filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)

        # Date Filter
        date_filter = self.request.GET.get('date_filter')
        today = timezone.now().date()
        
        if date_filter == 'today':
            queryset = queryset.filter(date__date=today)
        elif date_filter == 'this_week':
            week_end = today + timedelta(days=7)
            queryset = queryset.filter(date__date__range=[today, week_end])
        elif date_filter == 'this_weekend':
            # Get next weekend
            saturday = today + timedelta((5 - today.weekday()) % 7)
            sunday = saturday + timedelta(days=1)
            queryset = queryset.filter(
                Q(date__date=saturday) | Q(date__date=sunday)
            )
        elif date_filter == 'next_week':
            next_week_start = today + timedelta(days=7)
            next_week_end = next_week_start + timedelta(days=7)
            queryset = queryset.filter(date__date__range=[next_week_start, next_week_end])

        # Location Filter
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(
                Q(city__icontains=location) |
                Q(state__icontains=location)
            )

        return queryset.order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        
        # Add active filters to context
        context['active_filters'] = {
            'category': self.request.GET.get('category', ''),
            'date_filter': self.request.GET.get('date_filter', ''),
            'location': self.request.GET.get('location', '')
        }
        
        return context
    

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data here
        context['related_events'] = Event.objects.filter(
            category=self.object.category,
            date__gte=timezone.now()
        ).exclude(id=self.object.id)[:3]
        return context
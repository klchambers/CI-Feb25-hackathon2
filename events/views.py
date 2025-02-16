from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Event, EventCategory
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import redirect
import logging
from .forms import EventForm

import logging
from django.views.generic import ListView
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Event, EventCategory

logger = logging.getLogger(__name__)

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True)

        # Search Functionality from Navbar
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location_name__icontains=search_query) |
                Q(city__icontains=search_query)
            )
            logger.info(f"User searched for: {search_query}")

        # My Events Filter
        if self.request.GET.get('my_events') and self.request.user.is_authenticated:
            queryset = queryset.filter(created_by=self.request.user)

        # Category Filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)

        # Enhanced Location Filter
        location = self.request.GET.get('location', '').strip().lower()
        if location:
            location_query = Q()
            location_parts = location.split()
            for part in location_parts:
                location_query |= (
                    Q(city__icontains=part) |
                    Q(state__icontains=part) |
                    Q(zip_code__icontains=part) |
                    Q(address__icontains=part) |
                    Q(location_name__icontains=part)
                )
            queryset = queryset.filter(location_query)

        # Enhanced Date Filter
        date_filter = self.request.GET.get('date_filter')
        today = timezone.now().date()
        if date_filter:
            if date_filter == 'today':
                queryset = queryset.filter(date__date=today)
            elif date_filter == 'this_week':
                week_end = today + timedelta(days=7)
                queryset = queryset.filter(date__date__range=[today, week_end])
            elif date_filter == 'this_weekend':
                friday = today + timedelta((4 - today.weekday()) % 7)
                sunday = friday + timedelta(days=2)
                queryset = queryset.filter(date__date__range=[friday, sunday])
            elif date_filter == 'this_month':
                month_end = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                queryset = queryset.filter(date__date__range=[today, month_end])
            elif date_filter == 'next_month':
                next_month_start = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
                next_month_end = (next_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                queryset = queryset.filter(date__date__range=[next_month_start, next_month_end])
            elif date_filter == 'three_months':
                three_months = today + timedelta(days=90)
                queryset = queryset.filter(date__date__range=[today, three_months])

        # Store event counts for context
        self.total_events = Event.objects.filter(is_active=True).count()
        self.filtered_count = queryset.count()

        return queryset.order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()

        # Include active search and filter values in context
        context['active_filters'] = {
            'q': self.request.GET.get('q', ''),
            'category': self.request.GET.get('category', ''),
            'date_filter': self.request.GET.get('date_filter', ''),
            'location': self.request.GET.get('location', '')
        }

        # Event count information
        context['total_events'] = self.total_events
        context['filtered_count'] = self.filtered_count

        # User-specific event count
        if self.request.user.is_authenticated:
            context['user_events'] = Event.objects.filter(
                created_by=self.request.user,
                is_active=True
            ).count()

        # If no events found, suggest upcoming events
        if self.filtered_count == 0:
            context['suggested_events'] = Event.objects.filter(
                is_active=True,
                date__gte=timezone.now()
            ).order_by('date')[:3]

        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm  # Use the custom form
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.is_demo = False  # Ensure it's not a demo event
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'slug': self.object.slug})

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the event.")
        print("Form errors:", form.errors)  # Log errors
        print("POST data received:", self.request.POST)  # Log request data
        return self.render_to_response(self.get_context_data(form=form))

    
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'category', 'date', 'duration', 
              'location_name', 'address', 'city', 'state', 'zip_code', 
              'price', 'capacity', 'image']

    def test_func(self):
        """Only allow the event creator to edit."""
        event = self.get_object()
        return self.request.user == event.created_by

    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'slug': self.object.slug})

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')

    def test_func(self):
        """Only allow the event creator to delete."""
        event = self.get_object()
        return self.request.user == event.created_by

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Event deleted successfully!")
        return super().delete(request, *args, **kwargs)

    
class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context['can_edit'] = event.is_editable_by(self.request.user)
        context['related_events'] = Event.objects.filter(
            category=event.category,
            is_active=True,
            date__gte=timezone.now()
        ).exclude(id=event.id)[:3]
        return context
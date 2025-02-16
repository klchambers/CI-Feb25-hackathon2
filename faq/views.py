from django.shortcuts import render
from django.contrib import messages
from .models import Faq
from .forms import FaqForm


# Create your views here.
def faq(request):

    # Assign published FAQs to a variable
    published_faqs = Faq.objects.filter(published=True)

    # Initialising form
    form = FaqForm()

    if request.method == 'POST':
        form = FaqForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ submitted successfully!')
        else:
            messages.error(request, 'An error occurred while submitting the form.')

    context = {
        'published_faqs': published_faqs,
        'form': form
    }
    return render(request, 'faq/faq.html', context)
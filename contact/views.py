from django.shortcuts import render, redirect
from .forms import ContactForm

# Create your views here.
def contact(request):
    '''
    Render contact page and form
    '''
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            request.session['name'] = form.cleaned_data['name']
            request.session['email'] = form.cleaned_data['email']

            return redirect('contact_success')
    return render(request, 'contact/contact.html', {'form': form})


def contact_success(request):
    ''' display success message upon form submission '''
    name = request.session.get('name', 'User')
    email = request.session.get('email')
    return render(request, 'contact/contact_success.html', {'name': name, 'email': email})
from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect('index')
    else:
        form=CustomUserCreationForm()
    context={"form":form}
    return render(request, 'accounts/signup.html',context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Work, Author, Loan
from .forms import WorkSearchForm

def home(request):
    return render(request, 'catalog/home.html')

def work_list(request):
    form = WorkSearchForm(request.GET)
    works = Work.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            works = works.filter(
                Q(title__icontains=query) | 
                Q(authors__name__icontains=query)
            ).distinct()
    
    return render(request, 'catalog/work_list.html', {
        'works': works,
        'form': form
    })

def work_detail(request, pk):
    work = get_object_or_404(Work, pk=pk)
    return render(request, 'catalog/work_detail.html', {'work': work})

@login_required
def borrow_work(request, pk):
    work = get_object_or_404(Work, pk=pk)
    
    if not work.available:
        return redirect('catalog:work_detail', pk=pk)
    
    loan = Loan(work=work, user=request.user)
    loan.save()
    
    return redirect('catalog:my_loans')

@login_required
def return_work(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, user=request.user)
    
    if not loan.returned_date:
        loan.returned_date = timezone.now()
        loan.save()
    
    return redirect('catalog:my_loans')

@login_required
def my_loans(request):
    active_loans = Loan.objects.filter(user=request.user, returned_date=None)
    past_loans = Loan.objects.filter(user=request.user).exclude(returned_date=None)
    
    return render(request, 'catalog/my_loans.html', {
        'active_loans': active_loans,
        'past_loans': past_loans
    })

@login_required
def all_loans(request):
    if not request.user.is_staff:
        return redirect('catalog:home')
        
    loans = Loan.objects.all().order_by('-loan_date')
    users_with_loans = set(loan.user for loan in Loan.objects.filter(returned_date=None))
    
    return render(request, 'catalog/all_loans.html', {
        'loans': loans,
        'users_with_loans': users_with_loans
    })
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm


def home(request):

    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = ExpenseForm()

    total_expenses = Expense.objects.count()

    total_amount = Expense.objects.aggregate(
        Sum('amount')
    )['amount__sum']

    recent_expenses = Expense.objects.order_by('-date')[:5]

    return render(
        request,
        'expenses/home.html',
        {
            'form': form,
            'total_expenses': total_expenses,
            'total_amount': total_amount,
            'recent_expenses': recent_expenses,
        }
    )


def expense_list(request):

    expenses = Expense.objects.all().order_by('-date')

    return render(
        request,
        'expenses/expense_list.html',
        {
            'expenses': expenses
        }
    )
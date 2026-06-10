import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    if request.method == 'POST':
        expense.delete()
        return redirect('/list/')

    return render(
        request,
        'expenses/delete_expense.html',
        {
            'expense': expense
        }
    )
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():
            form.save()
            return redirect('/list/')

    else:

        form = ExpenseForm(
            instance=expense
        )

    return render(
        request,
        'expenses/edit_expense.html',
        {
            'form': form,
            'expense': expense
        }
    )
def export_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="expenses.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Date',
        'Category',
        'Description',
        'Amount'
    ])

    expenses = Expense.objects.all().order_by('-date')

    for expense in expenses:

        writer.writerow([
            expense.date,
            expense.category,
            expense.description,
            expense.amount
        ])

    return response
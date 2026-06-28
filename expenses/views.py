import csv

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ExpenseForm
from .models import Expense


def home(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Expense saved successfully!"
            )

            return redirect('/')

    else:
        form = ExpenseForm()

    total_expenses = Expense.objects.count()

    total_amount = Expense.objects.aggregate(
        Sum('amount')
    )['amount__sum']

    recent_expenses = Expense.objects.order_by('-date')[:5]

    category_totals = (
        Expense.objects
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('category')
    )

    return render(
        request,
        'expenses/home.html',
        {
            'form': form,
            'total_expenses': total_expenses,
            'total_amount': total_amount,
            'recent_expenses': recent_expenses,
            'category_totals': category_totals,
        }
    )


def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')

    search_query = request.GET.get('search')
    category_filter = request.GET.get('category')

    if search_query:
        expenses = expenses.filter(
            description__icontains=search_query
        )

    if category_filter:
        expenses = expenses.filter(
            category=category_filter
        )

    categories = [
        'Software',
        'Equipment',
        'Internet',
        'Office Supplies',
        'Mileage',
        'Advertising',
        'Education',
        'Travel',
        'Other',
    ]

    return render(
        request,
        'expenses/expense_list.html',
        {
            'expenses': expenses,
            'search_query': search_query,
            'category_filter': category_filter,
            'categories': categories,
        }
    )


def delete_expense(request, expense_id):
    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    if request.method == 'POST':
        expense.delete()

        messages.success(
            request,
            "Expense deleted successfully!"
        )

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

            messages.success(
                request,
                "Expense updated successfully!"
            )

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
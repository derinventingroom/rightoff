from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = [
            'date',
            'category',
            'description',
            'amount'
        ]
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01'
                }
            ),
        }
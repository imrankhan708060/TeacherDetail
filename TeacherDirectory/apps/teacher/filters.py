import django_filters
from . models import User
from django import forms
from ..accounts.models import Subject


class NameFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    subject = django_filters.ModelMultipleChoiceFilter(queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    class Meta:
        model=User
        fields=['last_name','subject']
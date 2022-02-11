import django_filters
from django_filters.filters import Filter
from django_filters.filterset import FilterSet
from .models import Asset, Breeding, Cow,Breed, DailyFeedUsage, DeadCow, Document, Donation,EmpAttendance,CowHealth, Expense, FeedEntry, Income, Milk, ProductUse, Production, SoldCow
from django.conf import settings


class CowFilter(django_filters.FilterSet):
    class Meta:
        model = Cow
        fields = ['tag_number','breed','gender','mother','status',]

class SoldCowFilter(django_filters.FilterSet):
    sold_date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = SoldCow
        fields = ['sold_date',] 


class AttendanceFilter(django_filters.FilterSet):
    attendance_date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = EmpAttendance
        fields = ['employee','attendance_date',]

class FeedUsageFilter(django_filters.FilterSet):    
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = DailyFeedUsage
        fields = ['feed','date',]

class ExpenseFilter(django_filters.FilterSet):    
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Expense
        fields = ['item','date',]

class IncomeFilter(django_filters.FilterSet):    
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Income
        fields = ['product','date']
class ProductionFilter(django_filters.FilterSet):   
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS) 
    class Meta:
        model = Production
        fields = ['product','date']

class MilkFilter(django_filters.FilterSet):    
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Milk
        fields = ['session','date']

class AssetFilter(django_filters.FilterSet):    
    purchase_date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Asset
        fields = ['asset_id','purchase_date']

class DocumentFilter(django_filters.FilterSet):    
    class Meta:
        model = Document
        fields = ['document_type']

class ProductUseFilter(django_filters.FilterSet):    
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = ProductUse
        fields = ['product','date']

class FeedEntryFilter(django_filters.FilterSet):    
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = FeedEntry
        fields = ['feed','supplier','date']

class DeadCowFilter(django_filters.FilterSet):    
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = DeadCow
        fields = ['date','cause_of_death',]

class BreedingFilter(django_filters.FilterSet):    
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Breeding
        fields = ['category','date',]

class DonationFilter(django_filters.FilterSet):    
    date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Donation
        fields = ['date',]

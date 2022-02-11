from itertools import filterfalse, product
from django import forms
from django.db import models
from django.forms import ValidationError, widgets
from django.forms.fields import DateField
from django.forms.models import ModelForm
from .models import Age, Asset, Breeding, Cow, DailyFeedUsage, DeadCow, Document, Donation,Employee, EmployeeSalary, Expense, Feed, FeedEntry, Income, Milk, PregnantCow, Product, ProductSale, ProductUse, Production, SoldCow,Supervisor, UNIT_CHOICES,User,Breed,EmpAttendance,CowHealth,FeedSupplier
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
import datetime
from django.utils import timezone
from django.db.models import Q

#Select options
GENDER_CHOICE = [
    ('','Select gender'),
    ('male','Male'),
    ('female','Female'),
]

"""Module Admin"""
#form of admin information 
class SupervisorForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        labels = {
            'password1':'Password',
            'password2':'Confirm Password'
        }

#form of admin update
class SupervisorUpdateForm(forms.ModelForm):
    def validate_date(date_value):
        if date_value > datetime.date.today():
            raise ValidationError("Enter valid date")
    first_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    date_of_join = forms.DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email')

#form of admin profile
class SupervisorProfileForm(forms.ModelForm):
    def validate_date(date_value):
        if date_value > datetime.date.today():
            raise ValidationError("Enter valid date")
    def validate_phone(phone):
        if len(phone) != 10:
            raise ValidationError("Enter valid phone number")

    date_of_birth = forms.DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    date_of_join = forms.DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    phone = forms.CharField(max_length=10,validators=[validate_phone])
    gender = forms.ChoiceField(choices=GENDER_CHOICE)

    class Meta():
        model = Supervisor
        fields = ('phone','gender','date_of_birth','address','profile_pic','date_of_join')
        labels = {
            'date_of_birth':'Date of Birth',
            'date_of_join':'Date Of Join'
        }

"""Module Employee"""
#Employee Forms
class EmployeeForm(forms.ModelForm):
    def validate_salary(salary):
        if salary < 0:
            raise ValidationError("Enter valid salary")
    def validate_aadhaar(aadhaar):
        if len(aadhaar) != 12:
            raise ValidationError("Enter valid Aadhaar number (must be 12 digit)") 
    def validate_bank(b_no):
        if len(b_no) < 8 or len(b_no) >16:
            raise ValidationError("Enter valid Bank account number")
    def validate_phone(phone):
        if len(phone) != 10:
            raise ValidationError("Enter valid phone number (must be 10 digit)")
    def validate_date(d_date):
        if d_date > datetime.date.today():
            raise ValidationError("Enter valid date")
    join_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,validators=[validate_date])
    date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,validators=[validate_date])
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    salary = forms.FloatField(required=True,validators=[validate_salary])
    aadhaar_no = forms.CharField(required=False,validators=[validate_aadhaar])
    bank_account_no = forms.CharField(required=False,validators=[validate_bank])
    phone = forms.CharField(required=True,validators=[validate_phone])
    class Meta():
        model = Employee
        fields = ('name','phone','gender','home','village','aadhaar_no','bank_account_no','date_of_birth','join_date','profile_pic','salary')

#Employee Update form
class EmployeeUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    join_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta():
        model = Employee
        fields = ('name','phone','gender','home','village','aadhaar_no','bank_account_no','date_of_birth','join_date','salary')

#Employee Attendance
class EmpAttendanceUpdateForm(forms.ModelForm):
    """Form definition for EmpAttendance."""

    class Meta:
        """Meta definition for EmpAttendanceform."""

        model = EmpAttendance
        fields = ('attendance',)

#salaru duration form
class SalaryDuration(forms.Form):
    """SalaryDuaration definition."""
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        cleaned_data =  super().clean()
        if start_date != None and end_date != None:
            if start_date > end_date:
                raise ValidationError("Enter valid dates")
            if EmployeeSalary.objects.filter(start_date = start_date).exists() or EmployeeSalary.objects.filter(end_date = start_date).exists() :
                raise ValidationError("Enter valid duration")
            last_salary = EmployeeSalary.objects.last()
            if last_salary != None:
                last_day = last_salary.end_date
                if start_date<last_day or end_date<last_day:
                    raise ValidationError("Enter valid duration")
            if EmployeeSalary.objects.filter(end_date = end_date).exists() or EmployeeSalary.objects.filter(start_date = end_date).exists() :
                raise ValidationError("Enter valid duration")
    


        return cleaned_data
    def validate_date(dt):
        if dt > datetime.date.today():
            raise ValidationError("Enter valid date")
    start_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,initial=datetime.date.today()-datetime.timedelta(days=6),validators=[validate_date],required=True)
    end_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,initial=datetime.date.today(),validators=[validate_date],required=True)

"""Module Cow"""
#Cow Forms
def get_mom_choice():
    MOM_CHOICES =  [
        ('','Select Cow'),
    ]
    mothers = Cow.objects.filter(~Q(status="Calf"),gender='female',is_dead=False,is_sold = False)
    for mom in mothers:
        name = mom.name
        MOM_CHOICES.append((name,name))
    return tuple(MOM_CHOICES)

def get_dad_choice():
    DAD_CHOICES = [
        ('','Select Cow')
    ]
    fathers = Cow.objects.filter(~Q(status="Calf"),gender='male',is_dead=False,is_sold = False)
    for dad in fathers:
        name = dad.name
        DAD_CHOICES.append((name,name))
    return tuple(DAD_CHOICES)
#form for new born calf
class NewBornCowForm(forms.ModelForm):  
    def validate_date(date_value):
        if date_value > datetime.date.today():
            raise ValidationError("Enter valid date")
    mother = forms.ChoiceField(choices = get_mom_choice,required=True) 
    father = forms.ChoiceField(choices=get_dad_choice,required=True)
    status = forms.CharField(disabled=True,initial='Calf')
    dob = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,validators=[validate_date])
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    class Meta():
        model = Cow
        fields = ('name','gender','breed','dob','mother','father','status')
        
    def __init__(self, *args, **kwargs):
        super(NewBornCowForm, self).__init__( *args, **kwargs)
        self.fields['breed'].empty_label = "Select a breed"
        self.fields['breed'].widget.choices =  self.fields['breed'].choices

class AgeForm(forms.ModelForm):
    """Form definition for Age."""

    class Meta:
        """Meta definition for Ageform."""

        model = Age
        fields =   '__all__'


#form for new brought cow
class NewBroughtCowForm(forms.ModelForm):
    def validate_age(age):
        if int(age) > 40 or int(age) < 0:
            raise ValidationError("Enter valid age")
    def validate_date(date_value):
        if date_value > datetime.date.today():
            raise ValidationError("Enter valid date")
    brought_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,validators=[validate_date])
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    brought_from = forms.CharField(required=True)

    class Meta():
        model = Cow
        fields = ('name','tag_number','gender','breed','brought_from','brought_date','status','vaccinated')
        labels ={
            'age_when_brought':'Age'
        }
    def __init__(self, *args, **kwargs):
        super(NewBroughtCowForm, self).__init__( *args, **kwargs)
        self.fields['breed'].empty_label = "Select a breed"
        self.fields['breed'].widget.choices =  self.fields['breed'].choices

#Cow/Calf Update
class CowUpdateForm(forms.ModelForm):
    dob = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,required=False)
    brought_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,required=False)
    class Meta():
        model = Cow
        fields = ('name','tag_number','dob','breed','gender','mother','father','status','brought_from','brought_date','vaccinated','is_dead','is_sold')
        labels = {
            'is_dead':'Dead',
            'is_sold':'Sold'
        } 

#Sold Cow Forms
class SoldCowForm(forms.ModelForm):
    """Form definition for SoldCow."""
    def validate_date(date_value):
        print("date sold_Cow ",date_value)
        if date_value > datetime.date.today():
            raise ValidationError("Enter valid date")
    sold_date = forms.DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for SoldCowform."""
        model = SoldCow
        fields = ('cow','sold_to','sold_address','sold_date','amount')

    def __init__(self, *args, **kwargs):
        super(SoldCowForm, self).__init__( *args, **kwargs)
        self.fields['cow'].queryset = Cow.objects.filter(~Q(status="Calf"),is_dead=False,is_sold=False)
        self.fields['cow'].empty_label = "Select cow"
        self.fields['cow'].widget.choices =  self.fields['cow'].choices

#Cow sale update form
class SoldCowUpdateForm(forms.ModelForm):
    """Form definition for SoldCow."""
    def validate_date(date_value):
        print("date sold_Cow ",date_value)
        if date_value > datetime.date.today():
            raise ValidationError("Enter valid date")
    sold_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,validators=[validate_date])
    class Meta:
        """Meta definition for SoldCowform."""
        model = SoldCow
        fields = ('sold_to','sold_address','sold_date','amount')

#Dead cow form
class DeadCowForm(forms.ModelForm):
    """Form definition for DeadCow."""
    def validate_date(date_value):
        if date_value > datetime.date.today():
            raise ValidationError("Enter valid date")
    date = forms.DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for DeadCowform."""
        model = DeadCow
        fields = ('cow','cause_of_death','date')

#Cow Health Form
class CowHealthForm(forms.ModelForm):
    """Form definition for CowHealth."""
    def clean(self):
        cleaned_data = super().clean()
        cow  = cleaned_data.get("cow")
        start_date =  cleaned_data.get("start_date")
        cured_date = cleaned_data.get('cured_date')
        disease = cleaned_data.get("disease")
        if cow ==None or start_date == None or disease == None:
            raise ValidationError("Enter the field")
        if cured_date !=None:
            if cured_date < start_date:
                raise ValidationError("Invalid date")
        return cleaned_data
    def validate_date(d_date):
        if d_date > datetime.date.today():
            raise ValidationError("Enter valid date")
    start_date = forms.DateField(validators=[validate_date],required=True,input_formats=settings.DATE_INPUT_FORMATS)
    cured_date = forms.DateField(required=False,validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for CowHealthform."""

        model = CowHealth
        fields = ('cow','disease','start_date','cured_date','doctor','medicine')
    def __init__(self, *args, **kwargs):
        super(CowHealthForm, self).__init__( *args, **kwargs)
        self.fields['cow'].queryset = Cow.objects.filter(is_dead=False,is_sold=False)
        self.fields['cow'].empty_label = "Select cow"
        self.fields['cow'].widget.choices =  self.fields['cow'].choices

"""Module Breed"""
#form for breed information
class BreedForm(forms.ModelForm):
    about = forms.Textarea()
    class Meta():
        model = Breed
        fields = ('title','about')

"""Module Product"""
#Form for product information
class ProductForm(forms.ModelForm):
    """Form definition for Product."""
    def validate_quantity(quantity):
        if quantity < 0:
            raise ValidationError("Enter valid quantity ")
    stock = forms.FloatField(validators=[validate_quantity])
    class Meta:
        """Meta definition for Productform."""
        model = Product
        fields = ('title','unit','stock','about')

#Production Form
class ProductionForm(forms.ModelForm):
    """Form definition for Production."""
    def validate_date(d_date):
        if d_date > datetime.date.today():
            raise ValidationError("Enter valid date")
    def validate_quantity(value):
        if value < 1 :
            raise ValidationError("Ener valid quantity")
    quantity = forms.FloatField(required=True,validators=[validate_quantity]) 
    date = forms.DateField(initial=timezone.now, required=True,validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)   
    class Meta:
        """Meta definition for Productionform."""

        model = Production
        fields = ('product','quantity','date')
    def __init__(self, *args, **kwargs):
        super(ProductionForm, self).__init__( *args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(~Q(title="Cow"),~Q(title="Milk"))
        self.fields['product'].empty_label = "Select Product"
#Product Usage form
class ProductUseForm(forms.ModelForm):
    """Form definition ProductUse."""
    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        date =  cleaned_data.get("date")
        product= cleaned_data.get("product")
        if product == None:
            raise ValidationError("Select product")
        if quantity == None:
            raise ValidationError("Enter Quantity")
        if date == None:
            raise ValidationError("Enter date")
        if date > datetime.date.today():
            raise ValidationError("Enter valid date")
        if quantity < 1:
             raise ValidationError("Quantity cannot be less than 1!")
        if quantity > product.stock:
            raise ValidationError(f"Enter valid quanityt (Stock: {product.stock} Kg)")
        return cleaned_data
    date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS) 
    class Meta:
        """Meta definition for DailyFeedUsageform."""
        model = ProductUse
        fields = ('product','quantity','date')
    def __init__(self, *args, **kwargs):
        super(ProductUseForm, self).__init__( *args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(~Q(title="Cow"),~Q(title="Milk"))
        self.fields['product'].empty_label = "Select Product"

#Product sale form
class ProductSaleForm(forms.ModelForm):
    """Form definition for ProductSale."""
    def clean(self):
        cleaned_data = super().clean()
        unit = cleaned_data.get("unit")
        product = cleaned_data.get("product")
        if unit > product.stock:
            raise ValidationError(f"Quantity exceeded the stock! (stock:{product.stock} {product.unit})")
    class Meta:
        """Meta definition for ProductSaleform."""

        model = ProductSale
        fields = '__all__'
        labels = {'unit':'Quantity'}
    def __init__(self, *args, **kwargs):
        super(ProductSaleForm, self).__init__( *args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(~Q(title="Cow"),~Q(title="Milk"))
        self.fields['product'].empty_label = "Select product"
        self.fields['product'].widget.choices =  self.fields['product'].choices

"""Module Income"""
#Income form
class IncomeForm(forms.ModelForm):
    """Form definition for Income."""
    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        date =  cleaned_data.get("date")
        product = cleaned_data.get("product")
        amount = cleaned_data.get("amount")
        if product == None:
            raise ValidationError("Enter Product")
        if quantity == None:
            raise ValidationError("Enter Quantity")
        if amount == None:
            raise ValidationError("Enter Amount")
        if date > datetime.date.today():
            raise ValidationError("Enter valid date")
        if quantity < 1 :
            raise ValidationError("Enter valid quantity")
        if quantity > product.stock:
            raise ValidationError(f"Enter valid quantity (stock: {product.stock} {product.unit})")
        return cleaned_data
    date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for Incomeform."""
        model = Income
        fields = '__all__'

"""Module Expense"""
#Expense form
class ExpenseForm(forms.ModelForm):
    """Form definition for Expense."""
    def validate_quantity(value):
        if value < 1:
            raise ValidationError("Enter valid quntity")
    def validate_date(d_date):
        if d_date>datetime.date.today():
            raise ValidationError("Enter valid date")
    quantity = forms.FloatField(validators=[validate_quantity],required=False)
    amount  = forms.FloatField(validators=[validate_quantity])
    date  = forms.DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for Expenseform."""

        model = Expense
        fields = ('item','quantity','unit','date','amount')

"""Module Milk"""
#Milk Form
class MilkForm(forms.ModelForm):
    """Form definition for Milk."""
    def clean(self):
        cleaned_data = super().clean()
        for data in cleaned_data.values():
            if data == None:
                raise ValidationError("Enter fields")
        if cleaned_data.get("date") > datetime.date.today():
            raise ValidationError("Enter valid date")
        session = cleaned_data.get("session")
        date =  cleaned_data.get("date")
        if Milk.objects.filter(session=session,date=date).exists():
            raise ValidationError("Session already added")
        if session == "Evening":
            if Milk.objects.filter(session="Morning",date=date).exists() == False:
                raise ValidationError("Enter Morning Session Milk Information")
        return cleaned_data 
    def validate_milk_quantity(value):
        if value < 0:
            raise ValidationError("Enter valid quanity")
    def validate_milk_income(value):
        if value < 0:
            raise ValidationError("Enter valid income")
    calf_use = forms.FloatField(validators=[validate_milk_quantity])
    employee_use = forms.FloatField(validators=[validate_milk_quantity])
    local_sale = forms.FloatField(validators=[validate_milk_quantity])
    dairy_sale = forms.FloatField(validators=[validate_milk_quantity])
    dairy_sale_income = forms.FloatField(validators=[validate_milk_income])
    local_sale_income = forms.FloatField(validators=[validate_milk_income])
    date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for Milkform."""

        model = Milk
        fields = ('date','session','calf_use','employee_use','local_sale','local_sale_income','dairy_sale','dairy_sale_income')
        labels = {'calf_use':'Calf User (Ltr)'}
#MIlk Update Form
class MilkUpdateForm(forms.ModelForm):
    """Form definition for Milk."""
    def clean(self):
        cleaned_data = super().clean()
        for data in cleaned_data.values():
            if data == None:
                raise ValidationError("Enter fields")
        return cleaned_data 
    def validate_milk_quantity(value):
        if value < 0:
            raise ValidationError("Enter valid quanity")
    def validate_milk_income(value):
        if value < 0:
            raise ValidationError("Enter valid income")
    calf_use = forms.FloatField(validators=[validate_milk_quantity])
    employee_use = forms.FloatField(validators=[validate_milk_quantity])
    local_sale = forms.FloatField(validators=[validate_milk_quantity])
    dairy_sale = forms.FloatField(validators=[validate_milk_quantity])
    dairy_sale_income = forms.FloatField(validators=[validate_milk_income])
    local_sale_income = forms.FloatField(validators=[validate_milk_income])
    class Meta:
        """Meta definition for Milkform."""

        model = Milk
        fields = ('calf_use','employee_use','local_sale','local_sale_income','dairy_sale','dairy_sale_income')

"""Module Feed"""
#Feed Form
class FeedForm(forms.ModelForm):
    """Form definition for Feed."""
    def validate_quanity(q):
        if q < 0:
            raise ValidationError("Enter valid quantity")
    stock = forms.FloatField(required=True,validators=[validate_quanity])
    class Meta:
        """Meta definition for Feedform.""" 
        model = Feed
        fields = ('title','stock','about')
        labels = { ' stock':'Stock (kg/ltr)'}

#Feed Supplier Form
class FeedSupplierForm(forms.ModelForm):
    """Form definition for FeedSupplier."""

    class Meta:
        """Meta definition for FeedSupplierform."""

        model = FeedSupplier
        fields = '__all__'
        labels = { ' GST_no':'GST Number'}

#Feed Entry Form
class FeedEntryForm(forms.ModelForm):
    """Form definition for FeedStockEntry."""
    def validate_date(d_date):
        if d_date > datetime.date.today():
            raise ValidationError("Enter valid date ")
    date = forms.DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for FeedStockEntryform."""

        model = FeedEntry
        fields = ('supplier','feed','date','bags','bag_weight','quantity','feed_rate','payment')
        labels = {
            'quantity':'Total Quantity(in Kg)',
            'feed_rate':'Rate (per Bag)',
            'payment':'Amount Paid'
        }

#Feed entry update form
class FeedEntryUpdateForm(forms.ModelForm):
    """Form definition for FeedEntryUpdate."""
    class Meta:
        """Meta definition for FeedEntryUpdateform."""
        model = FeedEntry
        fields = ('bags','bag_weight','quantity','feed_rate','payment')

#Daily Feed Usage Form
class DailyFeedUsageForm(forms.ModelForm):
    """Form definition for DailyFeedUsage."""
    def clean(self):
        cleaned_data = super().clean()
        feed_quantity = cleaned_data.get("quantity")
        date =  cleaned_data.get("date")
        feed= cleaned_data.get("feed")
        if feed == None:
            raise ValidationError("Select Feed")
        if feed_quantity == None:
            raise ValidationError("Enter Quantity")
        if date == None:
            raise ValidationError("Enter date")
        if date > datetime.date.today():
            raise ValidationError("Enter valid date")
        if feed_quantity < 1:
             raise ValidationError("Quantity cannot be less than 1!")
        if feed_quantity > feed.stock:
            raise ValidationError(f"Enter valid quanityt (Stock: {feed.stock} Kg)")
        return cleaned_data
    date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for DailyFeedUsageform."""
        model = DailyFeedUsage
        fields = ('feed','quantity','date')
    def __init__(self, *args, **kwargs):
        super(DailyFeedUsageForm, self).__init__( *args, **kwargs)
        self.fields['feed'].queryset = Feed.objects.all()
        self.fields['feed'].empty_label = "Select Feed"

"""Asset Module"""
#Assets Form
class AssetForm(forms.ModelForm):
    """Form definition for Asset."""
    def validate_date(date_value):
        if date_value > datetime.date.today():
            raise ValidationError("Enter a valid date")
    def validate_amount(amount):
        if amount < 0:
            raise ValidationError("Enter a valid amount")
    purchase_date = forms.DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    amount = forms.DecimalField(validators=[validate_amount])
    class Meta:
        """Meta definition for Assetform."""

        model = Asset
        fields = '__all__'

"""Module Documetns"""
class DocumentForm(forms.ModelForm):
    """Form definition for Document."""

    class Meta:
        """Meta definition for Documentform."""

        model = Document
        fields = '__all__'

"""Module Breeding"""
class BreedingForm(forms.ModelForm):
    """Form definition for Breeding."""
    def clean(self):
        cleaned_data = super().clean()
        cow = cleaned_data.get("cow")
        if cow == None:
            raise ValidationError("Enter cow")
        else:
            if PregnantCow.objects.filter(cow=cow).exists():
                raise ValidationError("Entered cow is pregnant")
    def validate_date(date_value):
        if date_value > datetime.date.today():
            raise ValidationError("Enter valid date")
    date = DateField(validators=[validate_date],input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for Breedingform."""
        model = Breeding
        fields = ('cow','date','category','stud','breed')
    def __init__(self, *args, **kwargs):
        super(BreedingForm, self).__init__( *args, **kwargs)
        self.fields['cow'].queryset = Cow.objects.filter(~Q(status="Calf"),gender="female",is_dead=False,is_sold=False)
        self.fields['cow'].empty_label = "Select Cow"
        self.fields['stud'].queryset = Cow.objects.filter(~Q(status="Calf"),gender="male",is_dead=False,is_sold=False)
        self.fields['stud'].empty_label = "Select Stud"

RESULT = [
        ('Successful','Successful'),
        ('Unsuccessful','Unsuccessful')
    ]
class BreedingUpdateForm(forms.ModelForm):
    """Form definition for BreedingUpdate."""
    result = forms.ChoiceField(required=True,choices=RESULT)
    class Meta:
        """Meta definition for BreedingUpdateform."""

        model = Breeding
        fields = ('result',)

class DonationForm(forms.ModelForm):
    """Form definition for Donation."""
    date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        """Meta definition for Donationform."""

        model = Donation
        fields = '__all__'



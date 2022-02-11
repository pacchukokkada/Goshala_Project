from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models import base
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, FloatField, TextField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone, tree
from dateutil.relativedelta import MO, relativedelta
import datetime
import os


GENDER_CHOICES = [
        ('male','Male'),
        ('female','Female'),
       
    ]
DOCUMENT_CHOICES = [
    ('Cow','Cow'),
    ('Employee','Employee'),
    ('Monthly Report','Monthly Report'),
    ('Invoice','Invoice'),
    ('other','Other'),
]
EXPENSE_CHOICES = [
    ('Paddy Straw','Paddy Straw'), 
    ('Feed','Feed'),
    ('Areca Leaf Powder','Areca Leaf Powder'),
    ('Medicine','Medicine'),
    ('Salary','Salary'),
    ('Current Bill','Current Bill'),
    ('NewsPaper Bill','NewsPaper Bill'),
    ('Repair & Maintainance','Repair & Maintainance'),
    ('Food','Food'),
    ('Transport','Transport'),
    ('Other','Other')

]
UNIT_CHOICES = [
    ('Kg','KG'),
    ('Litre','Litre'),
    ('Bundle','Bundle'),
    ('KM','KM'),
    ('Box','Box'),
    ('Bag','Bag'),
    ('Packet','Packets'),
    ('--','Other')
]
CAUSE_CHOICES = [
    ('Normal','Normal'),
    ('Disease','Disease'),
    ('Accident','Accident'),
    ('Other','Other'),
]

class Age(models.Model):
    """Model definition for Age."""
    year = models.IntegerField( null=True,blank=True)
    month = models.IntegerField(null=True,blank=True)
    day = models.IntegerField(null=True,blank=True)
    class Meta:
        """Meta definition for Age."""

        verbose_name = 'Age'
        verbose_name_plural = 'Ages'

    def __str__(self):
        """Unicode representation of Age."""
        return str(self.year)+" years "+str(self.month)+" months "+str(self.day)+" days"
    def save(self,*args,**kwargs):
        if self.day == None:
            self.day = 0
        if self.month == None:
            self.month = 0
        if self.year == None:
            self.year = 0
        super().save(*args,**kwargs)


"""Table for admin information """
class Supervisor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6,default='male')
    profile_pic = models.FileField(upload_to='images/',null=True,blank=True)
    date_of_join = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.user.first_name +" "+self.user.last_name

"""Table for breed information"""
class Breed(models.Model):
    title = models.CharField(max_length=50)
    about = models.TextField(max_length=300,null=True,blank=True)
    def __str__(self):
        return self.title

"""Table fot cow information"""
class Cow(models.Model):
    stages = [
        ('','Select a status'),
        ('Calf','Calf'),
        ('Hiefer','Hiefer'),
        ('Cow','Cow'),
        ('Bull','Bull'),
    ]
    duartion_type = [
        ('Day','Day'),
        ('Month','Month'),
        ('Year','Year')
    ]
    name = models.CharField(max_length=30,unique=True)
    tag_number = models.CharField(max_length=50,unique=True,null=True,blank=True)
    cow_age = models.ForeignKey(Age,on_delete=models.SET_NULL,null=True,related_name="age")
    dob = models.DateField(null=True,blank=True)
    breed = models.ForeignKey(Breed,on_delete=models.SET_NULL,null=True)
    gender = models.CharField(max_length=6,choices=GENDER_CHOICES)
    mother = models.CharField(max_length=30,null=True,blank=True)
    father = models.CharField(max_length=30,null=True,blank=True)
    status = models.CharField(choices=stages,max_length=30)
    cow_age_when_brought = models.ForeignKey(Age,on_delete=models.SET_NULL,null=True,related_name="age_when_brought",blank=True)
    brought_from = models.CharField(max_length=50,null=True,blank=True)
    brought_date = models.DateField(null=True,blank=True)
    vaccinated = models.BooleanField(default=False)
    is_dead = models.BooleanField(default=False)
    is_brought = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # def save(self,*args,**kwargs):
    #     if self.age_when_brought !=None:
    #         self.is_brought = True 
    #         if self.age == None:
    #             self.age = self.age_when_brought
    #     super().save(*args,**kwargs)

"""Table fot cow health information"""
class CowHealth(models.Model):
    """Model definition for CowHealth."""
    cow = models.ForeignKey(Cow,on_delete=models.CASCADE)
    disease = models.CharField(max_length=50,null=False)
    start_date = models.DateField()
    cured_date = models.DateField(null=True,blank=True)
    doctor = models.CharField(max_length=50,null=True,blank=True)
    medicine = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        """Unicode representation of CowHealth."""
        return self.cow.name+" disease: "+self.disease

"""Table for sold cow information"""
class SoldCow(models.Model):
    """Model definition for SoldCow."""
    cow = models.ForeignKey(Cow,on_delete=models.SET_DEFAULT,default="Deleted Cow")
    sold_to = models.CharField(max_length=30)
    sold_address = models.TextField(max_length=100)
    sold_date = models.DateField()
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    returned = models.BooleanField(default=False)

    def __str__(self):
        """Unicode representation of SoldCow."""
        return self.cow.name

"""Table for employee Information"""
class Employee(models.Model):
    WORK_CHOICE = [
        ('working','Working'),
        ('not_working','Not Working'),
    ]
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6)
    home = models.CharField(max_length=30)
    village = models.CharField(max_length=30)
    aadhaar_no = models.CharField(max_length=12,null=True,blank=True)
    bank_account_no = models.CharField(max_length=12,null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    join_date = models.DateField(null=True,blank=True)
    profile_pic = models.FileField(upload_to='images/',null=True,blank=True)
    salary = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.name +" "+self.home

"""Table for employee attendance"""
class EmpAttendance(models.Model):
    """Model definition for EmpAttendance."""
    attendance_types = [
        ('half','Half Day'),
        ('full','Full Day'),
        ('leave','Leave')
    ]
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    attendance_date =models.DateField(default=timezone.now,null=False)
    attendance = models.CharField(choices=attendance_types,max_length=8)
    is_added = models.BooleanField(default=False)

    def __str__(self):
        """Unicode representation of EmpAttendance."""
        return self.employee.name

"""Table fot feed information"""
class Feed(models.Model):
    """Model definition for Feed."""
    title = models.CharField(max_length=30,unique=True)
    stock = models.DecimalField(max_digits=7,decimal_places=2)
    about = models.TextField(max_length=100,null=True,blank=True)
    class Meta:
        """Meta definition for Feed."""

        verbose_name = 'Feed'
        verbose_name_plural = 'Feeds'

    def __str__(self):
        """Unicode representation of Feed."""
        return self.title

"""Table for Feed supplier"""
class FeedSupplier(models.Model):
    """Model definition for FeedSupplier."""
    title = models.CharField(max_length=30)
    address = models.TextField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    GST_no = models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        """Unicode representation of FeedSupplier."""
        return self.title

"""Table for Feed stock entry"""
class FeedEntry(models.Model):
    """Model definition for FeedEntry."""
    supplier = models.ForeignKey(FeedSupplier,on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed,on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    bags = models.DecimalField(max_digits=6,decimal_places=2)
    bag_weight = models.DecimalField(max_digits=5,decimal_places=2)
    quantity = models.DecimalField(max_digits=8,decimal_places=2)
    feed_rate = models.DecimalField(max_digits=6,decimal_places=2)
    payment = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        """Unicode representation of FeedEntry."""
        return self.supplier.title+" Date: "+str(self.date)

"""Table for daily feed Usage"""
class DailyFeedUsage(models.Model):
    """Model definition for DailyFeed."""

    feed = models.ForeignKey(Feed,on_delete=models.SET_DEFAULT,default="Deleted Feed")
    quantity = models.DecimalField(max_digits=5,decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        """Unicode representation of DailyFeed."""
        return self.feed.title+" "+str(self.used_date)

"""Table for asset information"""
class Asset(models.Model):
    """Model definition for  Assets."""
    asset_name = models.CharField(max_length=30)
    asset_id = models.CharField(unique=True,max_length=20)
    purchase_date  = models.DateField()
    amount = models.FloatField() 
    
    def __str__(self):
        """Unicode representation of  Assets."""
        return self.item_name


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.title, ext)
    return os.path.join(filename)

"""Table for document"""
class Document(models.Model):
    """Model definition for Document."""
    title = models.CharField(max_length=30)
    document_type = models.CharField(choices=DOCUMENT_CHOICES,max_length=15)
    file = models.FileField(upload_to=content_file_name)
    add_date = models.DateTimeField(auto_now=True)
    class Meta:
        """Meta definition for Document."""

        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        """Unicode representation of Document."""
        return self.title

"""Table for Expense information"""
class Expense(models.Model):
    """Model definition for Expens."""
    item = models.CharField(choices=EXPENSE_CHOICES,max_length=30)
    quantity = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    unit = models.CharField(choices=UNIT_CHOICES,max_length=30,null=True,blank=True)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        """Unicode representation of Expens."""
        return self.item+" Date: "+str(self.date)

"""Table for goshale Products"""
class Product(models.Model):
    """Model definition for Product."""
    title = models.CharField(max_length=30,unique=True)
    unit = models.CharField(choices=UNIT_CHOICES,max_length=30)
    stock = models.DecimalField(max_digits=8,decimal_places=2)
    about = models.TextField(max_length=100,null=True,blank=True)

    def __str__(self):
        """Unicode representation of Product."""
        return self.title

"Table for goshale production"
class Production(models.Model):
    """Model definition for Production."""
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8,decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        """Unicode representation of Production."""
        return self.product.title+" Date: "+str(self.date)    

"Table for income information"
class Income(models.Model):
    """Model definition for Income."""
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8,decimal_places=2)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        """Unicode representation of Income."""
        return self.product.title+" Date: "+str(self.date)

SESSION_CHOICES = [
    ('Morning','Morning'),
    ('Evening','Evening'),
]

"""Table for goshale milk production information"""
class Milk(models.Model):
    """Model definition for Milk."""
    date = models.DateField(default=timezone.now)
    session = models.CharField(choices=SESSION_CHOICES,max_length=10)
    calf_use = models.DecimalField(max_digits=5,decimal_places=2)
    employee_use = models.DecimalField(max_digits=5,decimal_places=2)
    local_sale = models.DecimalField(max_digits=5,decimal_places=2)
    local_sale_income = models.DecimalField(max_digits=5,decimal_places=2)
    dairy_sale = models.DecimalField(max_digits=5,decimal_places=2)
    dairy_sale_income = models.DecimalField(max_digits=5,decimal_places=2)
    total_milk = models.DecimalField(max_digits=5,decimal_places=2)
    total_income = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        """Unicode representation of Milk."""
        return "Date: "+str(self.date)+" Session:"+self.session

    def save(self,*args,**kwargs):
        self.total_milk = self.calf_use+self.employee_use+self.dairy_sale+self.local_sale
        self.total_income = self.local_sale_income+self.dairy_sale_income
        super().save(*args,**kwargs)


class CowCount(models.Model):
        """Model definition for CowCount."""
        breed = models.ForeignKey(Breed,on_delete=models.SET_DEFAULT,default="Deleted Breeed")
        akalu_count = models.IntegerField()
        gadasu_count = models.IntegerField()
        hori_count = models.IntegerField()
        male_calf_count = models.IntegerField()
        female_calf_count = models.IntegerField()
        sold_cow_count = models.IntegerField()
        dead_cow_count = models.IntegerField()
        total_count = models.IntegerField()
        class Meta:
            """Meta definition for CowCount."""
    
            verbose_name = 'CowCount'
            verbose_name_plural = 'CowCounts'
    
        def __str__(self):
            return self.breed.title
            
class ProductionDetail(models.Model):
    """Model definition for ProductionDetails."""
    product = models.ForeignKey(Product,on_delete=models.SET_DEFAULT,default="Deleted Product")
    production_quantity = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    sale_quantity = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    sale_amount = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    self_use = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    calf_use = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    remaining = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    class Meta:
        """Meta definition for ProductionDetail."""

        verbose_name = 'ProductionDetail'
        verbose_name_plural = 'ProductionDetails'

    def __str__(self):
        """Unicode representation of ProductionDetail."""
        return self.product.title

class ProductUse(models.Model):
    """Model definition for ProductUse."""
    product = models.ForeignKey(Product,on_delete=models.SET_DEFAULT,default="Deleted Product")
    quantity = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        """Unicode representation of ProductUse."""
        return self.product.title

class ExpenseDetail(models.Model):
    """Model definition for ExpenseDetail."""
    item = models.CharField(max_length=30)
    quantity = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    amount = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    class Meta:
        """Meta definition for ExpenseDetail."""

        verbose_name = 'ExpenseDetail'
        verbose_name_plural = 'ExpenseDetails'

    def __str__(self):
        """Unicode representation of ExpenseDetail."""
        return self.item

class CowExpenseDetail(models.Model):
    """Model definition for CowExpenseDetail."""
    total_cow = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    month_expense = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    one_cow_day_expense = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    all_cow_day_expense = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    one_cow_month_expense = models.DecimalField(max_digits=8,decimal_places=2,null=True)

    class Meta:
        """Meta definition for CowExpenseDetail."""

        verbose_name = 'CowExpenseDetail'
        verbose_name_plural = 'CowExpenseDetails'

    def __str__(self):
        """Unicode representation of CowExpenseDetail."""
        self.total_cow

"""Table for employee salary"""
class EmployeeSalary(models.Model):
    """Model definition for EmployeeSalary."""
    employee = models.ForeignKey(Employee,on_delete=models.SET_DEFAULT,default="Deleted Employee")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    attendance =models.DecimalField(max_digits=5,decimal_places=2,null=True)
    payable_salary = models.FloatField(null=True)
    is_paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True,blank=True)

    def __str__(self):
        """Unicode representation of EmployeeSalary."""
        return self.employee.name
    

"""Table for dead cow information"""
class DeadCow(models.Model):
    """Model definition for DeadCow."""
    cow = models.ForeignKey(Cow,on_delete=models.SET_DEFAULT,default="Deleted Cow")
    cause_of_death = models.CharField(choices=CAUSE_CHOICES,max_length=20)
    date = models.DateField(timezone.now)

    def __str__(self):
        """Unicode representation of DeadCow."""
        return self.cow.name+" Died:"+str(self.date)

    def save(self,*args,**kwargs):
        cow = Cow.objects.get(id=self.cow.id)
        cow.is_dead = True
        cow.save()
        super().save(*args,**kwargs)

"""Table fot product sale information"""
class ProductSale(models.Model):
    """Model definition for ProductSale."""
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    hsn = models.CharField(max_length=15)
    unit = models.DecimalField(max_digits=8,decimal_places=2)
    rate = models.DecimalField(max_digits=8,decimal_places=2)
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    cgst = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    sgst = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    igst = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    

    class Meta:
        """Meta definition for ProductSale."""

        verbose_name = 'ProductSale'
        verbose_name_plural = 'ProductSales'

    def __str__(self):
        """Unicode representation of ProductSale."""
        return self.product.title

"""Table for cow breeding information"""
class Breeding(models.Model):
    """Model definition for Bredding."""
    BREEDING_CATEGORY = [
        ('Natural','Natural'),
        ('Artificial Insemination','AI')
    ]
    RESULT = [
        ('Successful','Successful'),
        ('Unsuccessful','Unsuccessful')
    ]
    cow = models.ForeignKey(Cow,on_delete=models.SET_DEFAULT,default="Deleted cow",related_name="cow")
    date = models.DateField(default=timezone.now)
    category = models.CharField(choices=BREEDING_CATEGORY,max_length=25)
    stud = models.ForeignKey(Cow,on_delete=models.SET_NULL,null=True,blank=True,related_name="bull")
    breed = models.ForeignKey(Breed,on_delete=models.SET_NULL,null=True,blank=True)
    result = models.CharField(choices=RESULT,max_length=15,null=True,blank=True)
    
    
    def __str__(self):
        """Unicode representation of Bredding."""
        return self.cow.name+" Date:"+str(self.date)

class PregnantCow(models.Model):
    """Model definition for PregnantCow."""
    cow = models.ForeignKey(Cow,on_delete=models.CASCADE)
    calf_due = models.DateField(null=True,blank=True)
    def __str__(self):
        """Unicode representation of PregnantCow."""
        return self.cow.name

class Inbox(models.Model):
    """Model definition for Inbox."""
    name = models.CharField(max_length=25)
    email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=10)
    subject = models.CharField(max_length=25)
    message = models.TextField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False)


    def __str__(self):
        """Unicode representation of Inbox."""
        return self.name        

class Donation(models.Model):
    """Model definition for Donation."""
    donar_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    date = models.DateField()
    def __str__(self):
        """Unicode representation of Donation."""
        return self.donar_name++" "+str(self.date)
        

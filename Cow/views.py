from io import BytesIO
from django.contrib.auth import forms
from django.core.files.base import File
from django.db import reset_queries
from Cow.filters import AssetFilter, AttendanceFilter, BreedingFilter, CowFilter, DeadCowFilter, DocumentFilter, DonationFilter, ExpenseFilter, FeedEntryFilter, FeedUsageFilter, IncomeFilter, MilkFilter, ProductUseFilter, ProductionFilter, SoldCowFilter
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models.deletion import ProtectedError
from django.db.models.fields import DecimalField
from django.http.response import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from .models import Age, Asset, Breeding, Cow, CowExpenseDetail, DailyFeedUsage, DeadCow, Document, Donation, EmpAttendance,Employee, EmployeeSalary, Expense, ExpenseDetail, Feed, FeedEntry, FeedSupplier, Inbox, PregnantCow, ProductSale, ProductUse
from .models import Income, Milk, Product, Production, SoldCow,Supervisor,Breed,CowHealth,CowCount,ProductionDetail
import datetime
from dateutil.relativedelta import SU, relativedelta
from django.contrib import messages
from django.db.models import Sum
import calendar
import re
import decimal
from time import strptime, struct_time
from num2words import num2words
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic.edit import UpdateView
from .forms import AgeForm, AssetForm, BreedForm, BreedingForm, BreedingUpdateForm, CowHealthForm, CowUpdateForm, DailyFeedUsageForm, DeadCowForm, DocumentForm, DonationForm, EmpAttendanceUpdateForm, EmployeeForm, EmployeeUpdateForm, ExpenseForm, FeedEntryForm, FeedEntryUpdateForm, FeedForm, FeedSupplierForm, IncomeForm, MilkForm, MilkUpdateForm, NewBornCowForm, NewBroughtCowForm, ProductForm, ProductSaleForm, ProductUseForm, ProductionForm, SalaryDuration, SoldCowForm, SoldCowUpdateForm, SupervisorForm, SupervisorProfileForm,SupervisorUpdateForm, get_dad_choice, get_mom_choice
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View
import math
from django.urls import reverse
sum = 950
#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf 

#date format converts:
def dateConvert(date):
    return datetime.datetime.strptime (date, "%d/%m/%Y").strftime('%Y-%m-%d')

def areUSuperUser(user):
    if user.is_superuser:
        return True
    return False

#view for home page
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        inbox = Inbox.objects.create(name=name,email=email,phone=phone,subject=subject,message=message)
        inbox.save()
        return HttpResponse('success')
    else:
        context = {
            'product_count':Product.objects.all().count(),
            'cow_count':Cow.objects.filter(is_dead=False,is_sold=False).count(),
            'emp_count':Employee.objects.all().count(),
        }
    return render(request,'Home2/index.html',context)

#Dashboard 
@login_required()
def adminDashBorad(request):
    month = datetime.date
    calf_due_count = PregnantCow.objects.filter(calf_due__month = datetime.datetime.now().month,calf_due__year=datetime.datetime.now().year).count()
    health_count = CowHealth.objects.filter(cured_date=None).count()
    feed_count = Feed.objects.filter(stock__lte=50).count()
    inbox_count = Inbox.objects.filter(seen=False).count()
    pregnant_cows = PregnantCow.objects.all()
    count = 0
    for cow in pregnant_cows:
        if cow.calf_due < datetime.date.today():
            count +=1
    msgs = []
    if calf_due_count != 0:
        if calf_due_count ==1:
            msgs.append(f"{calf_due_count} cow has calf due this month")
        else:
            msgs.append(f"{calf_due_count} cows have calf due this month")
    if health_count != 0:
        if health_count == 1:
             msgs.append(f"{health_count} cow has health problem which is not recovered yet!")
        else:
            msgs.append(f"{health_count} cows have health problem which is not recovered yet!")
    if feed_count != 0:
        if feed_count == 1:
            msgs.append(f"{feed_count} feed has less stock please check")
        else:
            msgs.append(f"{feed_count} feeds have less stock please check")
    if inbox_count !=0:
        if inbox_count ==1:
             msgs.append(f"{inbox_count} unread message please check")
        else:
             msgs.append(f"{feed_count} unread messages please check")
    if count !=0:
        if count ==1:
             msgs.append(f"{count} pregnant cow exceeded calf due please check")
        else:
             msgs.append(f"{feed_count} upregnant cows exceeded calf due please check")
    breed_count = {}
    for breed in Breed.objects.all():
        count = Cow.objects.filter(is_dead=False,is_sold=False,breed=breed).count()
        breed_count[breed.title] = count
    context = {
        'employees' : Employee.objects.all(),
        'feeds':Feed.objects.all(),
        'cowhealths':CowHealth.objects.all().order_by('-start_date')[0:5],
        'requests':Inbox.objects.all().order_by('-date')[0:5],
        'products':Product.objects.all(),
        'cow_count':Cow.objects.filter(is_dead=False,is_sold=False,gender='female').count(),
        'bull_count':Cow.objects.filter(is_dead=False,is_sold=False,gender='male').count(),
        'pregnant_cows':PregnantCow.objects.all(),
        'inbox':Inbox.objects.filter(seen=False),
        'msgs':msgs,
        'breed_count':breed_count,
    }
    return render(request,'Cow/dashboard.html',context)

"""Module Admin"""
# add admin information
@login_required()
def addSupervisor(request):
    if request.user.is_superuser:
        if request.method == "POST":
            supervisor_form = SupervisorForm(request.POST)
            supervisor_profile_form = SupervisorProfileForm(request.POST,request.FILES)
            gender = request.POST.get('gender')
            if supervisor_form.is_valid() and supervisor_profile_form.is_valid():
                user = supervisor_form.save()
                user.save()
                profile = supervisor_profile_form.save(commit=False)
                profile.user = user
                profile.gender = gender
                profile.save()
                messages.success(request,'Admin information added successfully!')
                return redirect('Dashboard')
        else:
            supervisor_form = SupervisorForm()
            supervisor_profile_form = SupervisorProfileForm()
        
        context = {
            'supervisor_form':supervisor_form,
            'supervisor_profile_form':supervisor_profile_form,
        }
        return render(request,'Cow/admin_register.html',context)
    else:
        messages.warning(request,"You cannot add users!(Only superuser can add users)")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

#login of admin
def admin_login(request):
    msg= ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        
        if user:
            login(request,user)
            messages.success(request,'Admin logged in successfully!')
            return redirect('Dashboard')
        else:
            msg = "Wrong credentials!"
    return render(request,'Cow/admin_login.html',{'msg':msg})

#logout of admin
@login_required()
def admin_logout(request):
    logout(request)
    return redirect("Admin_login")

#user list
@login_required
def show_admin(request):
    admins = Supervisor.objects.all()
    return render(request,'Cow/show_admins.html',{'admins':admins})

#user pofile
@login_required
def show_user(request,id):
    admin = Supervisor.objects.get(id=id)
    return render(request,'Cow/admin_profile.html',{'admin':admin})

#show admin profile
@login_required()
def admin_profile(request):
    admin = Supervisor.objects.get(user=request.user)
    return render(request,'Cow/admin_profile.html',{'admin':admin})

#admin profile updation
@login_required()
def adminUpdate(request):
    user = request.user
    supervisor = Supervisor.objects.get(user=user)
    if request.method == "POST":
        supervisor_form = SupervisorUpdateForm(request.POST,instance=user)
        supervisor_profile_form = SupervisorProfileForm(request.POST,request.FILES,instance=supervisor)
        if supervisor_form.is_valid() and supervisor_profile_form.is_valid():
            user = supervisor_form.save()
            user.save()
            profile = supervisor_profile_form.save(commit=False)
            profile.user = user
            img = request.FILES.get("img")
            if img:
                profile.profile_pic =  img
            profile.save()
            messages.success(request,'Admin information updated successfully!')
            return redirect('Dashboard')
    else:
        supervisor_form = SupervisorUpdateForm(instance=user)
        supervisor_profile_form = SupervisorProfileForm(instance=supervisor)
    context = {
        'supervisor_form':supervisor_form,
        'supervisor_profile_form':supervisor_profile_form, 
        'pic':supervisor.profile_pic,    
    }
    return render(request,'Cow/edit_profile.html',context)
    
#Admin Password Change
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Cow/change_password.html', {
        'form': form
    })


"""Module Employee"""
#Add Employee
@login_required()
def addEmployee(request):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if request.method == 'POST':
            form  = EmployeeForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,'Employee added successfully!')
                return redirect('Display_emp')
        else:
            form = EmployeeForm()
        return render(request,'Cow/add_emp.html',{'form':form})

#Display Employee
@login_required()
def displayEmp(request):
    employees = Employee.objects.all()
    return render(request,'Cow/show_employee.html',{'employees':employees})
#Employee Updation
@login_required()
def employeeUpdate(request, id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        emp = Employee.objects.get(id=id)
        if request.method == "POST":
            emp_form = EmployeeUpdateForm(request.POST,request.FILES,instance=emp)
            img = request.FILES.get("img")
            if emp_form.is_valid():
                emp_form.save()
                if img !=None:
                    emp.profile_pic = img
                    emp.save()
                messages.success(request,'Employee updated successfully!')
                return redirect('Display_emp')
        else:
            emp_form = EmployeeUpdateForm(instance=emp)
        context = {
            'emp_form':emp_form,
            'pic':emp.profile_pic,    
        }
        return render(request,'Cow/edit_emp.html',context)        

#Employee Profile
@login_required()
def empProfile(request,id):
    emp = Employee.objects.get(id=id)
    return render(request,'Cow/emp_profile.html',{'emp':emp})

#Employee Deletion
@login_required()
def empDelete(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        emp = Employee.objects.get(id=id)
        emp.delete()
        messages.success(request,'Employee deleted successfully!')
    return redirect('Display_emp')
@login_required
def reroute(request):
    date = datetime.date.today()
    return redirect('Emp_attendance1',date=date)
#Employee Attendance
@login_required
def empAttendance(request,date=datetime.date.today()):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        attendance_date = date
        year, month, day = map(int, date.split('-'))
        # year = attendance_date.year
        # month = attendance_date.month
        # day = attendance_date.day
        attendance_date = datetime.date(year, month, day)  
        date  = request.GET.get("date")
        if date != None:
            if date != "":
                date = dateConvert(date)
                year, month, day = map(int, date.split('-'))
                date = datetime.date(year, month, day) 
                if date > datetime.date.today():
                    messages.warning(request,' Invalid date!')
                    return redirect('Emp_attendance') 
                attendance_date = date
        emp = Employee.objects.all()
        # is_attendance = EmpAttendance.objects.filter(attendance_date=datetime.date.today()).exists()
        # if is_attendance == False:
        #     for e in emp:
        #         attend = EmpAttendance(employee=e)
        #         attend.save()
        # attendance = EmpAttendance.objects.filter(attendance_date=datetime.date.today(),is_added=False)
        for e in emp:
            if EmpAttendance.objects.filter(employee=e,attendance_date=attendance_date).exists() == False:
                attend = EmpAttendance(employee=e,attendance_date=attendance_date)
                attend.save()
        attendance = EmpAttendance.objects.filter(attendance_date=attendance_date,is_added=False)
        context = {
            'emp':emp,
            'attendance':attendance,
            'date' : attendance_date,
            'year':year,
            'month':month,
            'day':day
        }
        return render(request,'Cow/emp_attendance.html',context)

#Add attendance
@login_required
def addAttendance(request,id):
    attend = request.POST.get('attendance')
    year = int(request.POST.get('year'))
    month = int(request.POST.get('month'))
    day = int(request.POST.get('day'))
    date = datetime.date(year,month,day)
    if id == '0':
        for emp in Employee.objects.all():
            attendance = EmpAttendance.objects.get(employee=emp,attendance_date=date)
            if attendance.attendance == "":
                print(attendance.attendance)
                attendance.attendance = attend
                attendance.is_added = True 
                attendance.save()
                print(emp.name)
    else:
        emp = Employee.objects.get(id=id)
        attendance = EmpAttendance.objects.get(employee=emp,attendance_date=date)
        attendance.attendance = attend
        attendance.is_added = True 
        attendance.save()
    return redirect('Emp_attendance1',date=date)

#Display attendance
@login_required
def attendanceList(request):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        attendance = EmpAttendance.objects.order_by('-attendance_date')
        attendance_filter = AttendanceFilter(request.GET,queryset=attendance)
        context = {
                'attendance':attendance_filter,
        }
        return render(request,'Cow/emp_attendance_list.html',context)

#Display MOnthly Attendace
@login_required
def monthlyAttendance(request):
    context = {}
    days =[]
    month = request.GET.get('month')
    year = request.GET.get('year')
    if month != None and year != None:
        if month == "":
            month = datetime.datetime.now().month
        else:
            month = int(month)
            year = int(year)
    else:
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
    emps =Employee.objects.all()
    attender ={}
    attendances = EmpAttendance.objects.filter(attendance_date__month=month,attendance_date__year=year).values('attendance_date').distinct().order_by('attendance_date')
    for d in attendances:
        days.append(d['attendance_date'].day)
    context['days']=days

    for emp in emps:
        for day in days:
            if EmpAttendance.objects.filter(employee=emp,attendance_date=datetime.date(year,month,day)).exists() ==False:
                attendance = EmpAttendance.objects.create(employee=emp,attendance_date=datetime.date(year,month,day))
                attendance.save()
    for emp in emps:
        attendances = EmpAttendance.objects.filter(employee=emp,attendance_date__month=month,attendance_date__year=year).order_by('attendance_date')
        attend = []
        for a in attendances:
            attend.append(a.attendance)
        attender[emp.name]=attend
    attendance = EmpAttendance.objects.filter(attendance_date__month=month,attendance_date__year=year).order_by('employee')
    context['attendance']=attendance
    context['attender'] = attender
    return render(request,'Cow/monthly_attendance.html',context)

#Update attendance
@login_required
def attendanceUpdate(request,id):
    attendance = EmpAttendance.objects.get(id=id)
    if request.method == "POST":
        form = EmpAttendanceUpdateForm(request.POST,instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('Emp_attendance_list')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += 'error'
    context={
        'form' : EmpAttendanceUpdateForm(instance=attendance),
        'attendance':attendance
    }
    return render(request,'Cow/emp_attendace_update.html',context)

#Employee Salary 
@login_required
def empSalaryGenerate(request):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        sal = sal = EmployeeSalary.objects.all().values("start_date","end_date").distinct().order_by('-end_date')
        if request.method == 'POST':
            form = SalaryDuration(request.POST)
            if form.is_valid():
                start_date = dateConvert(form['start_date'].value())
                end_date = dateConvert(form['end_date'].value())
                employee  = Employee.objects.all()
                for emp in employee:
                    full_atendance = EmpAttendance.objects.filter(employee=emp,attendance_date__range=[start_date,end_date],attendance="full").count()
                    half_attendance = EmpAttendance.objects.filter(employee=emp,attendance_date__range=[start_date,end_date],attendance="half").count()
                    attendance = full_atendance+(half_attendance*0.5)
                    if attendance != 0:
                        payable_salary = decimal.Decimal(attendance)*emp.salary
                        emp_salary = EmployeeSalary(employee=emp,start_date=start_date,end_date=end_date,attendance=attendance,payable_salary=payable_salary)
                        emp_salary.save()
                sal = EmployeeSalary.objects.all().values("start_date","end_date").distinct().order_by('-end_date')
                messages.success(request,'Salary duration added successfully!')
                return render(request,'Cow/employee_salary.html',{'form':form,'sal':sal})
        else:
            form = SalaryDuration()
            salaries = EmployeeSalary.objects.filter()
            emp_salaries = EmployeeSalary.objects.all().order_by('-end_date')
        return render(request,'Cow/employee_salary.html',{'form':form,'sal':sal})

#Employee salary detail
@login_required
def empSalaryDetail(request,start_date,end_date):
    date = re.split('. |, ',start_date)
    month_string = date[0]
    if len(date[0])>3:
        month_string = date[0][0:3]
    mon = strptime(month_string,'%b').tm_mon
    start_date = datetime.date(int(date[2]),int(mon),int(date[1]))
    date = re.split('. |, ',end_date)
    month_string = date[0]
    if len(date[0])>3:
        month_string = date[0][0:3]
    mon = strptime(month_string,'%b').tm_mon
    end_date = datetime.date(int(date[2]),int(mon),int(date[1]))
    
    emp_salaries = EmployeeSalary.objects.filter(start_date=start_date,end_date=end_date).order_by('-end_date')
    context = {
        'emp_salaries':emp_salaries,
        'start_date':start_date,
        'end_date':end_date,
    }
    return render(request,'Cow/employee_salary_detail.html',context)
    
#Employee salary pay
@login_required
def empSalaryPay(request):
    if request.method == 'GET':
        id = request.GET['post_id']
        payment = EmployeeSalary.objects.get(id=id)
        payment.is_paid = True
        payment.paid_on = datetime.date.today()
        payment.save()
        expense = Expense.objects.filter(item="salary",date=datetime.date.today()).exists()
        if expense == True:
            expense = Expense.objects.get(item="salary",date=datetime.date.today())
            expense.quantity += 1
            expense.amount += decimal.Decimal(payment.payable_salary)
        else:
            expense = Expense.objects.create(item="salary",date=datetime.date.today(),quantity=1,unit="--",amount=payment.payable_salary)
        expense.save()
        return HttpResponse(f'sucess!Amount {payment.payable_salary} paid to {payment.employee.name}')

#Salary Record Delete:
@login_required
def salaryDelete(request,start_date,end_date):
    date = re.split('. |, ',start_date)
    month_string = date[0]
    if len(date[0])>3:
        month_string = date[0][0:3]
    mon = strptime(month_string,'%b').tm_mon
    start_date = datetime.date(int(date[2]),int(mon),int(date[1]))
    date = re.split('. |, ',end_date)
    month_string = date[0]
    if len(date[0])>3:
        month_string = date[0][0:3]
    mon = strptime(month_string,'%b').tm_mon
    end_date = datetime.date(int(date[2]),int(mon),int(date[1]))
    EmployeeSalary.objects.filter(start_date=start_date,end_date=end_date).delete()
    messages.success(request,'Salary record deleted successfuly')
    return redirect('Employee_salary')

#Unpaid
@login_required
def unpaid(request):
    if request.method == 'GET':
        id = request.GET['post_id']
        
        salary = EmployeeSalary.objects.get(id=id)
        salary.is_paid = False
        salary.save()
        expense = Expense.objects.get(item="salary",date=salary.paid_on)
        print(expense)
        expense.quantity -= 1
        expense.amount -= decimal.Decimal(salary.payable_salary)
        expense.save()
        return HttpResponse('Payment successfully unpaid')

"""Module Cow"""
#ADD Cow
@login_required()
def addCow(request,cow):
    register = False
    age_form = ""
    if request.method == 'POST':
        if cow == '2':
            form = NewBornCowForm(request.POST)
            if form.is_valid():
                form.save()
                cattle = Cow.objects.get(name=form['name'].value())
                dob = cattle.dob
                dif = datetime.date.today()-dob
                sum = dif.days
                years = math.floor(sum / 365);
                months = math.floor((sum - (years * 365))/30.5);
                days = (sum - (years * 365) - (months * 30.5))
                age = Age.objects.create(year=years,month=months,day=days)
                age.save()
                cattle.cow_age = age
                cattle.save()
            else:
                return render(request,'Cow/add_calf.html',{'form':form})
        else:
            form = NewBroughtCowForm(request.POST)
            age_form = AgeForm(request.POST)  
            if form.is_valid() and age_form.is_valid():
                age = age_form.save()
                age.save()
                brought_cow = form.save(commit=False)
                brought_cow.cow_age_when_brought = age
                brought_cow.is_brought = True
                brought_cow.save()
            else:
                return render(request,'Cow/add_cow.html',{'form':form,'age_form':age_form})
        messages.success(request,'Cow added successfully!')
        return redirect('Display_cow')
    else:
        dad = get_dad_choice()
        mom = get_mom_choice()
        if cow == '2':
            form = NewBornCowForm()
            return render(request,'Cow/add_calf.html',{'form':form})
        else:
            form = NewBroughtCowForm()
            age_form = AgeForm()  
            context = {
                'form':form,
                'age_form':age_form,
                'register':register,
            }
            return render(request,'Cow/add_cow.html',context)
    

#Display Cow
@login_required()
def displayCow(request):
    if request.method == 'POST':
        cow_id = request.POST.get('cow_id')
        tag_no = request.POST.get('tag_no')
        print("Cow ID:",cow_id,"Tag NO: ",tag_no)
        cow = Cow.objects.get(id=cow_id)
        cow.tag_number = tag_no
        cow.save()
        return redirect('Display_cow')

    cow_list = Cow.objects.filter(is_dead=False,is_sold=False)
    cow_filter = CowFilter(request.GET,queryset=cow_list)
    return render(request,'Cow/show_cows.html',{'cow_filter':cow_filter})

    
#Cow Delete
@login_required()
def cowDelete(request, id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        cow = Cow.objects.get(id=id)
        in_soldcow = SoldCow.objects.filter(cow=cow).exists()
        in_health = CowHealth.objects.filter(cow=cow).exists()
        is_father = Cow.objects.filter(father=cow).exists()
        is_mother = Cow.objects.filter(mother=cow).exists()
        if in_soldcow ==True or in_health == True or is_father == True or is_mother ==True:
            messages.warning(request,'Cannot delete this cow! Referencd to another record.')
            return redirect('Cow_details',id=cow.id)
        else:
            cow.delete()
            messages.success(request,'Cow deleted successfully!')
            return redirect('Display_cow')
    

#Cow Update
@login_required
def cowUpdate(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        cow = Cow.objects.get(id=id)
        if request.method == 'POST':
            form = CowUpdateForm(request.POST,instance=cow)
            if form.is_valid():
                form.save()
                messages.success(request,'Cow updated successfully!')
                return redirect('Display_cow')
        else:
            form = CowUpdateForm(instance=cow)
        return render(request,'Cow/edit_cow.html',{'form':form})

#Cow Details
@login_required()
def cowDetails(request, id):
    cow = Cow.objects.get(id=id)    
    if cow.gender == "female":
        children = Cow.objects.filter(mother=cow.name)
    else:
        children = Cow.objects.filter(father=cow.name)

    context = {
        'cow' : cow,
        'health_details' : CowHealth.objects.filter(cow=cow),
        'children':children,
    }
    return render(request,'Cow/cow_profile.html',context)

#Cow Details by name
@login_required()
def cowDetailsByName(request, name):
    cow = Cow.objects.get(name=name)
    if cow.gender == "female":
        children = Cow.objects.filter(mother=cow)
    else:
        children = Cow.objects.filter(father=cow)
    context = {
        'cow' : cow,
        'health_details' : CowHealth.objects.filter(cow=cow),
        'children':children,
    }
    
    return render(request,'Cow/cow_profile.html',context)

#Add Sold Cow
@login_required
def addSoldCow(request):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if request.method == 'POST':
            form = SoldCowForm(request.POST)
            if form.is_valid():
                product = Product.objects.get(title="Cow")
                if Income.objects.filter(product=product,quantity=1,date=dateConvert(form['sold_date'].value())).exists() == False:
                    income = Income(product=product,quantity=1,date=dateConvert(form['sold_date'].value()), amount= decimal.Decimal(form['amount'].value()))
                else:
                    income = Income.objects.get(product=product,date=dateConvert(form['sold_date'].value()))
                    income.quantity +=1
                    income.amount += decimal.Decimal(form['amount'].value())
                income.save() 
                form.save()
                cow = Cow.objects.get(id= form['cow'].value())
                cow.is_sold = True
                cow.save()
                messages.success(request,'Record added successfully!')
                return redirect('Show_sold_cow')
        else:
            form = SoldCowForm()
        return render(request,'Cow/add_soldcow.html',{'form':form})

#Show Sold Cow
@login_required
def showSoldCow(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            sold_cows = SoldCow.objects.filter(sold_date__range=[start_date,end_date])
        else:
            sold_cows = SoldCow.objects.all().order_by('-sold_date')
    else:
        sold_cows = SoldCow.objects.all().order_by('-sold_date')
    
    sold_cow_filter = SoldCowFilter(request.GET,queryset=sold_cows)
    return render(request,'Cow/show_soldcow.html',{'sold_cow_filter':sold_cow_filter})

#Update Sold Cow
@login_required
def soldCowUpdate(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        sold_cow = SoldCow.objects.get(id=id)
        amount = sold_cow.amount
        date = sold_cow.sold_date
        if request.method == "POST":
            form = SoldCowUpdateForm(request.POST,instance=sold_cow)
            if form.is_valid():
                income = Income.objects.get(product__title="Cow",date=date)
                income.amount -=amount
                income.quantity -= 1
                income.save()
                if str(date) == str(form['sold_date'].value()):
                    income.amount += decimal.Decimal(form['amount'].value())
                    income.quantity += 1
                else:
                    if Income.objects.filter(product__title="Cow",date=dateConvert(form['sold_date'].value())).exists() == True:
                        income = Income.objects.get(product__title="Cow",date=dateConvert(form['sold_date'].value()))
                        income.amount +=decimal.Decimal(form['amount'].value())
                        income.quantity +=1
                    else:
                        product = Product.objects.get(title="Cow")
                        income = Income.objects.create(product=product,quantity=1,date=dateConvert(form['sold_date'].value()),amount=decimal.Decimal(form['amount'].value()))
                income.save()
                form.save()
                messages.success(request,'Record updated successfully!')
                return redirect('Show_sold_cow')
        else:
            form = SoldCowUpdateForm(instance=sold_cow)
        return render(request,'Cow/add_soldcow.html',{'form':form})

#Sold Cow Return 
@login_required
def soldCowReturn(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        sold_cow = SoldCow.objects.get(id=id)
        cow = Cow.objects.get(id=sold_cow.cow.id)
        sold_cow.returned = True
        sold_cow.save()
        cow.is_sold = False
        cow.save()
        messages.success(request,'Cow returned successfully!')
        return redirect('Show_sold_cow')

# Delete Sold Cow
@login_required
def soldCowDelete(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        sold_cow = SoldCow.objects.get(id=id)
        cow = Cow.objects.get(name=sold_cow.cow.name)
        cow.is_sold = False
        product = Product.objects.get(title="Cow")
        income = Income.objects.get(product=product,date=sold_cow.sold_date)
        income.amount -=sold_cow.amount
        income.quantity -= 1
        income.save()
        cow.save()
        sold_cow.delete()
        messages.success(request,'Record deleted successfully!')
        return redirect('Show_sold_cow')

#Add Dead cow
@login_required
def addDeadCow(request):
    if request.method == 'POST':
        form = DeadCowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Record Added successfully!')
            return redirect('Show_dead_cow')
    else:
        form = DeadCowForm()
    return render(request,'Cow/add_dead_cow.html',{'form':form})

#Display Dead cow
@login_required
def showDeadCow(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            dead_cows = DeadCow.objects.filter(date__range=[start_date,end_date])
        else:
            dead_cows = DeadCow.objects.all().order_by('-date')
    else:
         dead_cows = DeadCow.objects.all().order_by('-date')
    context = {
        'dead_cow_filter' : DeadCowFilter(request.GET,queryset=dead_cows)
    }
    return render(request,'Cow/show_dead_cows.html',context)

#Update dead cow
@login_required
def deadCowUpdate(request,id):
    dead_cow = DeadCow.objects.get(id=id)
    cow = Cow.objects.get(id=dead_cow.cow.id)
    cow.is_dead = False
    if request.method == 'POST': 
        cow.save()
        form = DeadCowForm(request.POST,instance=dead_cow)
        if form.is_valid():
            form.save()
            messages.success(request,'Record Updated successfully!')
            return redirect('Show_dead_cow')
    else:
        form = DeadCowForm(instance=dead_cow)
    return render(request,'Cow/add_dead_cow.html',{'form':form})
    
#Dead Cow Delete
@login_required
def deadCowDelete(request,id):
    dead_cow = DeadCow.objects.get(id=id)
    cow = Cow.objects.get(id=dead_cow.cow.id)
    cow.is_dead = False
    cow.save()
    dead_cow.delete()
    messages.success(request,'Record Deleted successfully!')
    return redirect('Show_dead_cow')

#Add Cow Health Record
@login_required
def addCowHealthRecord(request):
    if request.method == "POST":
        form = CowHealthForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request,"Cow Health record added successfully!")
            return redirect('Cow_health_record_list')
    else:
        form = CowHealthForm()
    return render(request,'Cow/add_health_record.html',{'form':form})

#Display Cow Health Record
@login_required
def cowHealthRecordList(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            cow_health = CowHealth.objects.filter(start_date__range=[start_date,end_date])
        else:
            cow_health = CowHealth.objects.order_by('-start_date')
    else:
        cow_health = CowHealth.objects.order_by('-start_date')
    return render(request,'Cow/health_record_list.html',{'cow_health':cow_health})

#Display Details of Cow Health Record
@login_required
def cowHealthDetail(request,id):
    main_health_deatil = CowHealth.objects.get(id=id)
    all_health_details = CowHealth.objects.filter(cow=main_health_deatil.cow).exclude(id=id)
    context = {
        'main_health_detail':main_health_deatil,
        'all_health_details':all_health_details,
    }
    return render(request,'Cow/health_detail.html',context)

#Update Cow Health Record
@login_required
def cowHealthUpdate(request,id):
    cow_health = CowHealth.objects.get(id=id)
    if request.method == "POST":
        form = CowHealthForm(request.POST,instance=cow_health)
        if form.is_valid():
            form.save()
            messages.success(request,"Cow Health record updated successfully!")
            return redirect('Cow_health_details',id=id )
    context={
        'form' : CowHealthForm(instance=cow_health),
    }
    return render(request,'Cow/add_health_record.html',context)

#Delete Cow Health Record
@login_required
def cowHealthDelete(request,id):
    cow_health = CowHealth.objects.get(id=id)
    cow_health.delete()
    messages.success(request,"Cow Health record deleted successfully!")
    return redirect('Cow_health_record_list')

"""Module Breed"""
#Add Breed
@login_required()
def addBreed(request):
    event = " "
    if request.method == 'POST':
        breed_name = request.POST.get('breed_name')
        if breed_name !=None:
            breed = Breed(title=breed_name)
            breed.save()
            return HttpResponse('success')
        else:
            form = BreedForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Breed added successfully!')
                return redirect('Display_breed')
    else:
        form = BreedForm()
        event = "Add"
    return render(request,'Cow/add_breed.html',{'form':form,'event':event})

    


#Add Breed
@login_required()
def addBreedAjax(request):
    form = BreedForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_breed");</script>' % (instance.pk, instance))
    return render(request, 'Cow/add_breed.html', {"form" : form})

#Display Breed
@login_required()
def breedList(request):
    breeds = Breed.objects.all()
    return render(request,'Cow/breed_list.html',{'breeds':breeds})

#Delete Breed
@login_required()
def breedDelete(request,id):
    breed = Breed.objects.get(id=id)
    if Cow.objects.filter(breed=breed).exists():
        messages.warning(request,'Cannot delete this breed refrenced to other recoed!')
    else:
        breed.delete()
        messages.success(request,'Breed deleted successfully!')
    return redirect('Display_breed')
#Update Breed
@login_required
def breedUpdate(request,id):
    breed = Breed.objects.get(id=id)
    if request.method == 'POST':
        form = BreedForm(request.POST,instance=breed)
        if form.is_valid():
            form.save()
            messages.success(request,'Breed updated successfully!')
            return redirect('Display_breed')
    else:
        event = "Update"
        form = BreedForm(instance=breed)
    return render(request,'Cow/add_breed.html',{'form':form,'event':event})

"""Module Product"""
#Add Products
@login_required
def addProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Product added successfully!')
            return redirect('Show_product')
    else:
        form = ProductForm()
    return render(request,'Cow/add_products.html',{'form':form})

#Display Products
@login_required
def showProducts(request):
    products = Product.objects.all()
    return render(request,'Cow/show_products.html',{'products':products})

#Update Products
@login_required
def productsUpdate(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        product = Product.objects.get(id=id)
        if request.method == "POST":
            form = ProductForm(request.POST,instance=product)
            if form.is_valid():
                form.save()
                messages.success(request,'Product updated successfully!')
                return redirect('Show_product')
        else:
            form = ProductForm(instance=product)
        return render(request,'Cow/add_products.html',{'form':form})

#Delete Products
@login_required
def productsDelete(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        product = Product.objects.get(id=id)
        in_income = Income.objects.filter(product=product).exists()
        in_production = Production.objects.filter(product=product).exists()
        if in_income == True or in_production == True:
            messages.warning(request,f'Cannot delete {product.title}! Referenced to other record.')
        else:
            product.delete()
            messages.success(request,'Product added successfully!')
        return redirect('Show_product')

"""Production"""
#Add Production
@login_required
def addProduction(request):
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(id=form['product'].value())
            product.stock += decimal.Decimal(form['quantity'].value())
            product.save()
            form.save()
            messages.success(request,'Production added successfully!')
            return redirect('Show_production')
    else:
        form = ProductionForm()
    return render(request,'Cow/add_production.html',{'form':form})

#Show Production
@login_required
def showProduction(request):
    productions = Production.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            productions = Production.objects.filter(date__range=[start_date,end_date])
        else:
            productions = Production.objects.all().order_by('-date')
    else:
        productions = Production.objects.all().order_by('-date')
    production_filter = ProductionFilter(request.GET,queryset=productions)
    return render(request,'Cow/show_production.html',{'production_filter':production_filter})

#Update production
@login_required
def productionUpdate(request,id):
    production = Production.objects.get(id=id)
    quantity = production.quantity
    product = Product.objects.get(title=production.product)
    if request.method == "POST":
        form = ProductionForm(request.POST,instance=production)
        if form.is_valid():
            product.stock -=quantity
            product.save()
            product = Product.objects.get(id=form['product'].value())
            product.stock += decimal.Decimal(form['quantity'].value())
            product.save()
            form.save()
            messages.success(request,'Production updated successfully!')
            return redirect('Show_production')
    else:
        form = ProductionForm(instance=production)
    return render(request,'Cow/add_production.html',{'form':form})

#Delete Production
@login_required
def productionDelete(request,id):
    production = Production.objects.get(id=id)
    product = Product.objects.get(title=production.product)
    product.stock -=production.quantity
    product.save() 
    production.delete()
    messages.success(request,'Production deleted successfully!')
    return redirect('Show_production')

"""Product Usage"""
#Add Product use
@login_required
def addProductUse(request):
    if request.method == 'POST':
        form = ProductUseForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(id=form['product'].value())
            product.stock -= decimal.Decimal(form['quantity'].value())
            product.save()
            form.save()
            messages.success(request,'Product Usage added successfully!')
            return redirect('Show_product_use')
    else:
        form = ProductUseForm()
    return render(request,'Cow/add_product_use.html',{'form':form})
#Display Product Use
@login_required
def showProductUse(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            product_usages = ProductUse.objects.filter(date__range=[start_date,end_date])
        else:
            product_usages = ProductUse.objects.all()
    else:
         product_usages = ProductUse.objects.all()
    product_usage__filter = ProductUseFilter(request.GET,queryset=product_usages)
    return render(request,'Cow/show_product_use.html',{'product_usage__filter':product_usage__filter})

#Upddate Product Use
@login_required
def productUseUpdate(request,id):
    product_usage = ProductUse.objects.get(id=id)
    qu = product_usage.quantity
    product = Product.objects.get(title=product_usage.product)
    if request.method == 'POST':
        form = ProductUseForm(request.POST,instance=product_usage)
        if form.is_valid():
            #old product stock update
            product.stock +=qu
            product.save()
            #new product stock update
            product = Product.objects.get(id=form['product'].value())
            product.stock -= decimal.Decimal(form['quantity'].value())
            product.save()
            form.save()
            messages.success(request,'Product Usage updated successfully!')
            return redirect('Show_product_use')
    else:
        form = ProductUseForm(instance=product_usage)
    return render(request,'Cow/add_product_use.html',{'form':form})

#Delete Product Use
@login_required
def productUseDelete(request,id):
    product_usage = ProductUse.objects.get(id=id)
    product = Product.objects.get(title=product_usage.product)
    product.stock +=product_usage.quantity
    product.save()
    product_usage.delete()
    messages.success(request,'Product Usage deleted successfully!')
    return redirect('Show_product_use')

"""Product Sale"""
#Add Product to cart
@login_required
def addCartProduct(request,option):
    if request.method == 'POST':
        form = ProductSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Product_cart')
    else:
        if option == "1":
            ProductSale.objects.all().delete()
        form = ProductSaleForm()
    return render(request,'Cow/add_product_sale.html',{'form':form})

#Display products in cart
@login_required
def productCart(request):
    context = {
        'sale':ProductSale.objects.all(),
        'total': ProductSale.objects.all().aggregate(Sum('amount'))
    }
    return render(request,'Cow/show_product_sale.html',context)

#Deleted Product from cart
@login_required
def cartProductDelete(request,id):
    sale_product = ProductSale.objects.get(id=id)
    sale_product.delete()
    messages.success(request,'Product removed form cart!')
    return redirect('Product_cart') 

#Deleted Product from cart
@login_required
def allCartProductDelete(request):
    ProductSale.objects.all().delete()
    return redirect('Product_cart') 


#update cart product
@login_required
def cartProductUpdate(request,id):
    product = ProductSale.objects.get(id=id)
    if request.method == 'POST':
        form = ProductSaleForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('Product_cart')
    else:
        form = ProductSaleForm(instance=product)
    return render(request,'Cow/add_product_sale.html',{'form':form})
#Billing
def billing(request):
    sold_products = ProductSale.objects.all()
    sub_total = ProductSale.objects.all().aggregate(Sum('amount'))
    cgst = ProductSale.objects.all().aggregate(Sum('cgst'))
    sgst =  ProductSale.objects.all().aggregate(Sum('sgst'))
    igst =  ProductSale.objects.all().aggregate(Sum('igst'))
    gst = cgst['cgst__sum']+sgst['sgst__sum']+igst['igst__sum']
    taxable_value = int(sub_total['amount__sum']) - int(request.POST['discount'])
    total = taxable_value + taxable_value*(gst/100) 
    total_in_words = num2words(total)
    for product in sold_products:
        item = Product.objects.get(title=product.product.title)
        item.stock -=  product.unit
        item.save()
        income = Income.objects.create(product=product.product,date=datetime.date.today(),quantity=product.unit,amount=total)
        income.save()
    context = {
        'date':datetime.date.today(),
        'billed_to': request.POST['billed_to'],
        'shipped_to': request.POST['shipped_to'],
        'name':request.POST['name'],
        'ship_name':request.POST['ship_name'],
        'address':request.POST['address'],
        'ship_address':request.POST['ship_address'],
        'gstn':request.POST['gstn'],
        'ship_gstn':request.POST['ship_gstn'],
        'sub_total':sub_total['amount__sum'],
        'discount':request.POST['discount'],
        'cgst': cgst['cgst__sum'],
        'sgst':sgst['sgst__sum'],
        'igst':igst['igst__sum'],       
        'taxable_value':taxable_value,
        'tax_amount':gst,
        'total_amount':total,
        'products':ProductSale.objects.all(),
        'tatal_amount_in_words':total_in_words,
    }
    pdf = render_to_pdf('Cow/invoice.html',context)
    if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s_%s.pdf"%(context['name'],context['date'])
            #download = request.GET.get('download')
            content = "inline; filename=%s " % (filename)
            response['Content-Disposition'] = content
            report_file = BytesIO(pdf.content)
            document = Document.objects.create(title=f"Invoice {context['name']} {datetime.date.today()}",file=File(report_file, filename),document_type='Invoice')
            document.save()
            ProductSale.objects.all().delete()
            return response
    else:
            return HttpResponse("Not found")

    """MOdule Income"""
#Add Income
@login_required
def addIncome(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(id=form['product'].value())
            product.stock -= decimal.Decimal(form['quantity'].value())
            product.save()
            form.save()
            messages.success(request,'Income added succeddfully!')
            return redirect('Show_income')
    else:
        form = IncomeForm()
    return render(request,'Cow/add_income.html',{'form':form})

#Display Income
@login_required
def showIncome(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            incomes = Income.objects.filter(date__range=[start_date,end_date])
        else:
            incomes = Income.objects.all().order_by('-date')
    else:
        incomes = Income.objects.all().order_by('-date')
    income_filter = IncomeFilter(request.GET,queryset=incomes)
    for income in incomes:
        if income.quantity <= 0 and income.amount <= 0:
            income.delete()
    return render(request,'Cow/show_income.html',{'income_filter':income_filter})

#Update Income
@login_required
def incomeUpdate(request,id):
    income = Income.objects.get(id=id)
    quantity = income.quantity
    product = Product.objects.get(title=income.product)
    if request.method == "POST":
        form = IncomeForm(request.POST,instance=income)
        if form.is_valid(): 
            product.stock += quantity
            product.save()
            product = Product.objects.get(id=form['product'].value())
            product.stock -= decimal.Decimal(form['quantity'].value())
            product.save()
            form.save()
            messages.success(request,'Income updated succeddfully!')
            return redirect('Show_income')
    else:
        form = IncomeForm(instance=income)
    return render(request,'Cow/add_income.html',{'form':form})

#Delete Income
@login_required
def incomeDelete(request,id):
    income = Income.objects.get(id=id)
    product = Product.objects.get(title=income.product)
    product.stock +=income.quantity
    product.save() 
    income.delete()
    messages.success(request,'Income deleted succeddfully!')
    return redirect('Show_income')

"""Module Expense"""
#Add Expense
@login_required
def addExpenes(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Expense added successfuly!')
            return redirect('Show_expense')
    else:
        form = ExpenseForm()
    return render(request,'Cow/add_expense.html',{'form':form})

#Display Expense
@login_required
def showExpense(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            expenses = Expense.objects.filter(date__range=[start_date,end_date])
        else:
            expenses = Expense.objects.all().order_by('-date')
    else:
        expenses = Expense.objects.all().order_by('-date')
    #delete unnecessary expense
    for expense in expenses:
        if expense.quantity == 0 and expense.amount == 0:
            expense.delete()
    expense_filter = ExpenseFilter(request.GET,queryset=expenses)
    return render(request,'Cow/show_expense.html',{'expense_filter':expense_filter})

#Update Expense
@login_required
def expenseUpdate(request,id):
    expense = Expense.objects.get(id=id)
    if request.method == "POST":
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request,'Expense updated successfuly!')
            return redirect('Show_expense')
    else:
        form = ExpenseForm(instance=expense)
    return render(request,'Cow/add_expense.html',{'form':form})

#Delete Expense
@login_required
def expenseDelete(request,id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    messages.success(request,'Expense deleted successfuly!')
    return redirect('Show_expense')

"""Module Milk"""
#Add Milk
@login_required
def addMilk(request):
    if request.method == 'POST':
        form = MilkForm(request.POST)
        if form.is_valid():
            product_milk = Product.objects.get(title="Milk")
            total_milk = int(form['dairy_sale'].value())+int(form['local_sale'].value())+int(form['employee_use'].value())+int(form['calf_use'].value())
            total_income = int(form['dairy_sale_income'].value())+int(form['local_sale_income'].value()) 
            is_today_milk = Milk.objects.filter(date=dateConvert(form['date'].value()),session="Morning").exists()
            if is_today_milk ==True:
                today_milk = Milk.objects.filter(date=dateConvert(form['date'].value()),session="Morning")
                for milk in today_milk:
                    total_milks = total_milk+milk.total_milk
                    total_income = total_income+milk.total_income
                    today_milk_income = Income.objects.get(product=product_milk,date=dateConvert(form['date'].value()))
                    today_milk_income.quantity = total_milks
                    today_milk_income.amount = total_income
                    today_milk_income.save()

            else:
                income = Income(product =product_milk,quantity=total_milk,date=dateConvert(form['date'].value()),amount=total_income)    
                income.save()
            if Production.objects.filter(product=product_milk,date=dateConvert(form['date'].value())):
                production = Production.objects.get(product=product_milk,date=dateConvert(form['date'].value()))
                print(production.quantity,"+",total_milk)
                production.quantity += decimal.Decimal(total_milk)
                print("second qu: ",production.quantity)
                production.save()
            else:
                production = Production.objects.create(product=product_milk,date=dateConvert(form['date'].value()),quantity=decimal.Decimal(total_milk))
                production.save()
            form.save()
            messages.success(request,'Milk Production/Distribution record added successfully!')
            return redirect('Show_milk')
    else:
        form = MilkForm()
    return render(request,'Cow/add_milk.html',{'form':form})

#Display Milk
@login_required
def showMilk(request):
    milks = Milk.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            milks = Milk.objects.filter(date__range=[start_date,end_date])
        else:
            milks = Milk.objects.all().order_by('-date')
    else:
        milks = Milk.objects.all().order_by('-date')
    milk_filter = MilkFilter(request.GET,queryset=milks)
    return render(request,'Cow/show_milk.html',{'milk_filter':milk_filter})

#Update Milk
@login_required
def milkUpdate(request,id):
    milk = Milk.objects.get(id=id)
    milk_income = milk.total_income
    milk_quantity = milk.total_milk
    milk_date = milk.date
    if request.method == "POST":
        form = MilkUpdateForm(request.POST,instance=milk)
        if form.is_valid():
            income = Income.objects.get(product__title="Milk",date=milk_date)
            income.quantity -= milk_quantity
            income.amount -= milk_income
            income.quantity += decimal.Decimal(form['dairy_sale'].value())+decimal.Decimal(form['local_sale'].value())+decimal.Decimal(form['employee_use'].value())+decimal.Decimal(form['calf_use'].value())
            income.amount += decimal.Decimal(form['dairy_sale_income'].value())+decimal.Decimal(form['local_sale_income'].value()) 
            income.save()
            production = Production.objects.get(product__title="Milk",date=milk_date)
            production.quantity -= milk_quantity
            production.quantity += decimal.Decimal(form['dairy_sale'].value())+decimal.Decimal(form['local_sale'].value())+decimal.Decimal(form['employee_use'].value())+decimal.Decimal(form['calf_use'].value())
            production.save()
        form.save()
        messages.success(request,'Milk Production/Distribution record updated successfully!')
        return redirect('Show_milk')
    else:
        form = MilkUpdateForm(instance=milk)
    return render(request,'Cow/add_milk.html',{'form':form})

#Delete Milk
@login_required
def milkDelete(request,id):
    milk = Milk.objects.get(id=id)
    milk_date = milk.date
    income = Income.objects.get(product__title ="Milk", date=milk_date)
    income.quantity -= milk.total_milk
    income.amount -= milk.total_income
    income.save()
    production = Production.objects.get(product__title="Milk",date=milk_date)
    production.quantity -= milk.total_milk
    production.save()
    milk.delete()
    messages.success(request,'Milk Production/Distribution record deleted successfully!')
    return redirect('Show_milk')

"""Module Feed"""
#Add Feed
@login_required
def addFeedInfo(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Feed added successfully!')
            return redirect('Feed_list')
    else:
        form = FeedForm()
    return render(request,'Cow/add_feed_info.html',{'form':form})

#Display Feed
@login_required
def showFeed(request):
    feeds = Feed.objects.all()
    return render(request,'Cow/show_feeds.html',{'feeds':feeds})

#Update Feed
@login_required
def feedUpdate(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        feed = Feed.objects.get(id=id)
        if request.method == "POST":
            form = FeedForm(request.POST,instance=feed)
            if form.is_valid():
                form.save()
                messages.success(request,'Feed updated successfully!')
                return redirect('Feed_list')
        context={
            'form' : FeedForm(instance=feed),
        }
        return render(request,'Cow/add_feed_info.html',context)

#Delete Feed
@login_required
def feedDelete(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        feed = Feed.objects.get(id=id)
        in_stock_entry = FeedEntry.objects.filter(feed=feed).exists()
        in_feed_usage = DailyFeedUsage.objects.filter(feed=feed).exists()
        if in_stock_entry == True or in_feed_usage ==True:
            messages.warning(request,'Cannot delete this feed! Referenced to other record.')
        else: 
            feed.delete()    
            messages.success(request,'Feed deleted successfully!')
        return redirect('Feed_list')

#Add Supplier
@login_required
def addFeedSupplier(request):
    if request.method == 'POST':
        form = FeedSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Feed Supplier added successfully!')
            return redirect('Supplier_list')
    else:
        form = FeedSupplierForm()
    return render(request,'Cow/add_feed_suppliers.html',{'form':form})

#Display Supliers
def showFeedSupplier(request):
    suppliers = FeedSupplier.objects.all()
    return render(request,'Cow/show_feed_supplier.html',{'suppliers':suppliers}) 

#Update Suppliers
@login_required
def feedSupplierUpdate(request,id):
    supplier = FeedSupplier.objects.get(id=id)
    if request.method == "POST":
        form = FeedSupplierForm(request.POST,instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request,'Feed Supplier updated successfully!')
            return redirect('Supplier_list')
    context={
        'form' : FeedSupplierForm(instance=supplier),
    }
    return render(request,'Cow/add_feed_suppliers.html',context)

#Delete Suppliers
@login_required
def feedSupplierDelete(request,id):
    supplier = FeedSupplier.objects.get(id=id)
    if FeedEntry.objects.filter(supplier=supplier).exists() == True:
        messages.warning(request,'Cannot deleted supplier! Referenced to other record.')
    else:
        supplier.delete()
        messages.success(request,'Feed deleted successfully!')
    return redirect('Supplier_list')

#Add Stock Entry
@login_required
def addFeedStockEntry(request):
    if request.method == 'POST':
        form = FeedEntryForm(request.POST)
        if form.is_valid():
            date = datetime.datetime.strptime (form['date'].value(), "%d/%m/%Y").strftime('%Y-%m-%d')
            if Expense.objects.filter(item='Feed',date=date).exists() == True:
                expense = Expense.objects.get(item='Feed',date=form['date'].value())
                expense.quantity +=decimal.Decimal(form['quantity'].value())
                expense.amount += decimal.Decimal(form['payment'].value())
            else:
                expense = Expense.objects.create(item="Feed",quantity=decimal.Decimal(form['quantity'].value()),unit="Kg",date=date,amount=decimal.Decimal(form['payment'].value()))
            expense.save()
            feed = Feed.objects.get(id=form['feed'].value())
            feed.stock += decimal.Decimal(form['quantity'].value())
            feed.save()
            form.save()
            messages.success(request,'Feed Stock Entry added successfully!')
            return redirect('Feed_stock_entry_list')
    else:
        form = FeedEntryForm()
    return render(request,'Cow/add_feed_stock_entry.html',{'form':form})


#Display Stock Entry
@login_required
def showFeedEntry(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            feed_entry = FeedEntry.objects.filter(date__range=[start_date,end_date])
        else:
            feed_entry = FeedEntry.objects.all().order_by('-date')
    else:
        feed_entry = FeedEntry.objects.all()
    feed_entry_filter = FeedEntryFilter(request.GET,queryset=feed_entry)
    return render(request,'Cow/show_feed_entry.html',{'feed_entry_filter':feed_entry_filter})

#Update Stock Entry
@login_required
def feedEntryUpdate(request,id):
    feed_entry = FeedEntry.objects.get(id=id)
    qu = feed_entry.quantity
    amonut = feed_entry.payment
    date = feed_entry.date
    if request.method == "POST":
        form = FeedEntryUpdateForm(request.POST,instance=feed_entry)
        if form.is_valid():
            feed = Feed.objects.get(title=feed_entry.feed.title)
            print(feed)
            feed.stock -=qu
            print(feed.stock)
            expense = Expense.objects.get(date=date,item="Feed")
            expense.quantity -= qu
            expense.amount -= amonut
            expense.quantity += decimal.Decimal(form['quantity'].value())
            expense.amount += decimal.Decimal(form['payment'].value())
            expense.save()
            feed.stock += decimal.Decimal(form['quantity'].value())
            print(feed.stock)
            feed.save()
            form.save()
            messages.success(request,'Feed Stock Entry updated successfully!')
            return redirect('Feed_stock_entry_list')
    else:
        form = FeedEntryUpdateForm(instance=feed_entry)
    return render(request,'Cow/add_feed_stock_entry.html',{'form':form})

#Delete Stock Entry
@login_required
def feedEntryDelete(request,id):
    feed_entry = FeedEntry.objects.get(id=id)
    feed = Feed.objects.get(title=feed_entry.feed)
    feed.stock -= feed_entry.quantity
    feed.save()
    expense = Expense.objects.get(item='Feed',date=feed_entry.date)
    expense.amount -= feed_entry.payment
    expense.quantity -= feed_entry.quantity
    expense.save()
    feed_entry.delete()
    messages.success(request,'Feed Stock Entry deleted successfully!')
    return redirect('Feed_stock_entry_list')

# Add  Daily Feed Usage
@login_required
def addDailyFeedUsage(request):
    if request.method == 'POST':
        form = DailyFeedUsageForm(request.POST)
        if form.is_valid():
            feed = Feed.objects.get(id=form['feed'].value())
            feed.stock = feed.stock - decimal.Decimal(form['quantity'].value())
            feed.save()
            form.save()
            messages.success(request, 'Feed usage added successfully!')
            return redirect('Show_feed_usage')
    else:
        form = DailyFeedUsageForm()
    return render(request,'Cow/add_feed_usage.html',{'form':form})

#Display Daily Feed Usage
@login_required
def showFeedUsage(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            feed_usages = DailyFeedUsage.objects.filter(date__range=[start_date,end_date])
        else:
            feed_usages = DailyFeedUsage.objects.all().order_by('-date')
    else:
        feed_usages = DailyFeedUsage.objects.all().order_by('-date')
    feed_usage_filter = FeedUsageFilter(request.GET,queryset=feed_usages)
    return render(request,'Cow/show_feed_usage.html',{'feed_usage_filter':feed_usage_filter})

#Update Daily Feed Usage
@login_required
def feedUsageUpdate(request,id):
    feed_usage = DailyFeedUsage.objects.get(id=id)
    qu = feed_usage.quantity
    feed = Feed.objects.get(title=feed_usage.feed)
    if request.method == "POST":
        form = DailyFeedUsageForm(request.POST,instance=feed_usage)
        if form.is_valid():
            feed.stock += qu
            feed.save()
            feed_new = Feed.objects.get(id=form['feed'].value())
            feed_new.stock -= decimal.Decimal(form['quantity'].value())
            feed_new.save()
            form.save()
            messages.success(request, 'Feed usage updated successfully!')
            return redirect('Show_feed_usage')
    else:
        form = DailyFeedUsageForm(instance=feed_usage)
    return render(request,'Cow/add_feed_usage.html',{'form':form})

#Delete Daily Feed Usage
@login_required
def feedUsageDelete(request,id):
    feed_usage = DailyFeedUsage.objects.get(id=id)
    feed = Feed.objects.get(title=feed_usage.feed)
    feed.stock += feed_usage.quantity
    feed.save()
    feed_usage.delete()
    messages.success(request, 'Feed usage Deleted successfully!')
    return redirect('Show_feed_usage')

"""Module Monthly Record"""
#Monthly Record
@login_required
def monthlyRecord(request):
    #Deleting Existing Data
    CowCount.objects.all().delete()
    ProductionDetail.objects.all().delete()
    ExpenseDetail.objects.all().delete()
    CowExpenseDetail.objects.all().delete()
    year = request.GET.get('year')
    month =request.GET.get('month')
    start_date = None
    end_date = None
    last_day=None
    if year != None and month != None:
        year = int(year)
        if month != "":
            month = int(month)
            start_date = datetime.date(year,month,1)
            last = calendar.manthrange(year,month)
            last_day = int(last[1])
            end_date = datetime.date(year,month,last_day)
        elif month == "":
            start_date = datetime.date(year,1,1)
            end_date = datetime.date(year,12,31)
    else:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        start_date = datetime.date(year,month,1)
        last = calendar.monthrange(year,month)
        last_day = int(last[1])
        end_date = datetime.date(year,month,last_day)
    breeds = Breed.objects.all()
    #Cow Attendance Report
    for breed in breeds:
        akalu_count = Cow.objects.filter(is_dead=False,is_sold=False,breed=breed,status="Cow",).count()
        gadasu_count = Cow.objects.filter(is_dead=False,is_sold=False,breed=breed,status="Hiefer").count()
        hori_count = Cow.objects.filter(is_dead=False,is_sold=False,breed=breed,status="Bull").count()
        male_calf_count  = Cow.objects.filter(is_dead=False,is_sold=False,breed=breed,status="Calf",gender="male").count()
        female_calf_count  = Cow.objects.filter(is_dead=False,is_sold=False,breed=breed,status="Calf",gender="female").count()
        sold_cow_count = SoldCow.objects.filter(sold_date__range=[start_date,end_date],cow__breed =breed).count()
        dead_cow_count = Cow.objects.filter(is_dead=True,is_sold=False,breed=breed).count()
        total_count = akalu_count+gadasu_count+hori_count+male_calf_count+female_calf_count+sold_cow_count+dead_cow_count
        cow_count = CowCount(breed=breed,akalu_count=akalu_count,gadasu_count=gadasu_count,hori_count=hori_count,
                             male_calf_count=male_calf_count,female_calf_count=female_calf_count,sold_cow_count=sold_cow_count,
                             dead_cow_count=dead_cow_count,total_count=total_count)
        cow_count.save()
    #Production/Income Report    
    products = Product.objects.all()
    for product in products: 
        if product.title == "Milk":
            production_quantity = Milk.objects.filter(date__range = [start_date,end_date]).aggregate(Sum('total_milk'))
            sale_amount = Milk.objects.filter(date__range = [start_date,end_date]).aggregate(Sum('total_income'))
            self_use = Milk.objects.filter(date__range = [start_date,end_date]).aggregate(Sum('employee_use'))
            calf_use =  Milk.objects.filter(date__range = [start_date,end_date]).aggregate(Sum('calf_use'))
            sale_quantity = None
            if production_quantity['total_milk__sum'] != None:
                sale_quantity = production_quantity['total_milk__sum']-self_use['employee_use__sum']-calf_use['calf_use__sum']
            production_details = ProductionDetail(product=product,production_quantity=production_quantity['total_milk__sum'],
                                                    sale_quantity=sale_quantity,sale_amount=sale_amount['total_income__sum'],
                                                    self_use=self_use['employee_use__sum'],calf_use=calf_use['calf_use__sum'],)
            production_details.save()                                    
        elif product.title == "Cow":
            sale_quantity = SoldCow.objects.filter(sold_date__range = [start_date,end_date]).count()
            sale_amount = SoldCow.objects.filter(sold_date__range = [start_date,end_date]).aggregate(Sum('amount'))
            production_details = ProductionDetail(product=product,sale_quantity=sale_quantity,
                                                    sale_amount=sale_amount['amount__sum'])
            production_details.save()
        else:  
            production_quantity = Production.objects.filter(product=product,date__range = [start_date,end_date]).aggregate(Sum('quantity'))
            sale_quantity = Income.objects.filter(product=product,date__range = [start_date,end_date]).aggregate(Sum('quantity'))
            sale_amount = Income.objects.filter(product=product,date__range = [start_date,end_date]).aggregate(Sum('amount'))
            self_use = ProductUse.objects.filter(product=product,date__range = [start_date,end_date]).aggregate(Sum('quantity'))
            remaining = None
            if production_quantity['quantity__sum'] != None:
                if sale_quantity['quantity__sum'] != None:
                    if self_use['quantity__sum'] != None:
                        remaining = production_quantity['quantity__sum'] - sale_quantity['quantity__sum'] -self_use['quantity__sum']
                    else:
                        remaining = production_quantity['quantity__sum'] - sale_quantity['quantity__sum'] 
                elif self_use['quantity__sum'] != None:
                        remaining = production_quantity['quantity__sum'] - self_use['quantity__sum']
                else:
                    remaining = production_quantity['quantity__sum']
            production_details = ProductionDetail(product=product,production_quantity=production_quantity['quantity__sum'],
                                                    sale_quantity=sale_quantity['quantity__sum'],sale_amount=sale_amount['amount__sum'],
                                                    self_use=self_use['quantity__sum'],remaining=remaining)
            production_details.save()

    #Expense Report
    items = [
            'Paddy Straw','Feed','Areca Leaf Powder','Medicine','Salary','Current Bill','NewsPaper Bill','Repair & Maintainance',
            'Food','Transport','Other',]
    for item in items:
        quantity = Expense.objects.filter(item=item,date__range = [start_date,end_date]).aggregate(Sum('quantity'))
        amount = Expense.objects.filter(item=item,date__range = [start_date,end_date]).aggregate(Sum('amount'))
        expense_details = ExpenseDetail(item=item,quantity=quantity['quantity__sum'],amount=amount['amount__sum'])
        expense_details.save()
    #month expense details

    if month != "":
        total_cow = Cow.objects.filter(is_dead=False,is_sold=False).count()
        month_expense = Expense.objects.filter(date__range = [start_date,end_date]).aggregate(Sum('amount'))
        one_cow_day_expense = 0
        if month_expense['amount__sum'] != None:
            one_cow_day_expense = (month_expense['amount__sum']/total_cow)/last_day
        all_cow_day_expense = one_cow_day_expense*total_cow
        one_cow_month_expense = one_cow_day_expense*last_day
        cow_expense = CowExpenseDetail(total_cow=total_cow,month_expense=month_expense['amount__sum'],one_cow_day_expense=one_cow_day_expense,
                                        all_cow_day_expense=all_cow_day_expense,one_cow_month_expense=one_cow_month_expense)
        cow_expense.save()
    context = {
        'cow_counts' : CowCount.objects.all(),
        'production_details' : ProductionDetail.objects.all(),
        'expense_details':ExpenseDetail.objects.all(),
        'cow_expense':CowExpenseDetail.objects.all(),
        'year':year,
        'month':month,
        
    }
    return render(request,'Cow/monthly_report.html',context)

#Print Page
@login_required
def printPage(request,option):
    context = {
        'cow_counts' : CowCount.objects.all(),
        'production_details' : ProductionDetail.objects.all(),
        'expense_details':ExpenseDetail.objects.all(),
        'cow_expense':CowExpenseDetail.objects.all(),
        'date':datetime.date.today()
        
    }
    pdf = render_to_pdf('Cow/report_print.html', context)
    if pdf:
        filename = "Report_%s.pdf"%(context['date']) 
        if option == "1":        
            report_file = BytesIO(pdf.content)
            document = Document.objects.create(title=f"Report {datetime.date.today()}",file=File(report_file, filename),document_type='Monthly Report')
            document.save()
            messages.success(request,'Report succesfully saved in database!')
            return redirect("Show_month_report")
        elif option == "2":
            response = HttpResponse(pdf, content_type='application/pdf')
            #download = request.GET.get('download')
            content = "inline; filename=%s " % (filename)
            response['Content-Disposition'] = content
            return response
    else:
        return HttpResponse("Not found")


"""Module Asset"""
#Add Assets
@login_required
def addAssets(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Asset added successfully!')
            return redirect('Show_asset')
    else:
        form = AssetForm()
    return render(request,'Cow/add_assets.html',{'form':form})

#Display Assets
@login_required
def showAssets(request):
    assets = Asset.objects.all()
    asset_filter = AssetFilter(request.GET,queryset=assets)
    return render(request,'Cow/show_assets.html',{'asset_filter':asset_filter})

#Update Assets
@login_required
def assetUpdate(request,id):
    asset = Asset.objects.get(id=id)
    if request.method == 'POST':
        form = AssetForm(request.POST,instance=asset)
        form.save()
        messages.success(request,'Asset updated successfully!')
        return redirect('Show_asset')
    else:
        form = AssetForm(instance=asset)
    return render(request,'Cow/add_assets.html',{'form':form})

#Delete Assets
@login_required
def assetDelete(request,id):
    asset = Asset.objects.get(id=id)
    asset.delete()
    messages.success(request,'Asset deleted successfully!')
    return redirect('Show_asset')

"""Module Documents"""
#Add Documents
@login_required
def addDocuments(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Document added successfully!')
            return redirect('Show_document')
    else:
        form = DocumentForm()
    return render(request,'Cow/add_documents.html',{'form':form})

#Display Documents
@login_required
def showDocuments(request):
    start_date = request.GET.get('start_date')
    end_date =   request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            print(start_date)
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            documents = Document.objects.filter(add_date__range=[datetime.datetime.combine(start_date, datetime.time.min),datetime.datetime.combine(end_date, datetime.time.max)])
        else:
            documents = Document.objects.all()
    else:
        documents = Document.objects.all()
    
    filter_documents = DocumentFilter(request.GET,queryset=documents)
    return render(request,'Cow/file.html',{'filter_documents':filter_documents})

#Update Document
@login_required
def documentUpdate(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        document = Document.objects.get(id=id)
        if request.method == 'POST':
            form = DocumentForm(request.POST,instance=document)
            if form.is_valid():
                form.save()
                messages.success(request,'Document updated leted successfully!')
                return redirect('Show_document')
        else:
            form = DocumentForm(instance=document)
        return render(request,'Cow/add_documents.html',{'form':form})

#Delete Document
@login_required
def documentDelete(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'You cannot access!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        document = Document.objects.get(id=id)
        document.delete()
        messages.success(request,'Document deleted successfully!')
        return redirect('Show_document')

"""Monthly Income/Expense/Milk Chart"""
def income_chart(request):
    labels = []
    income_data = []
    expense_data = []
    milk_data = []
    current_month_num = datetime.datetime.now().month
    months = []
    for i in range(7):
        months.append(current_month_num-i)
    months.reverse()
    for month in months:
        year = datetime.datetime.now().year
        if month < 1:
            if month == 0:
                month = 12
                year -= 1
            else:
                month = 12+month
                year -=1
        month_abre = datetime.date(2015, month, 1).strftime('%b')
        labels.append(month_abre)
        income = Income.objects.filter(date__year=year,date__month=month).aggregate(Sum('amount'))
        expense = Expense.objects.filter(date__year=year,date__month=month).aggregate(Sum('amount'))
        milk_production = Milk.objects.filter(date__year=year,date__month=month).aggregate(Sum('total_milk'))
        if income['amount__sum'] == None: income['amount__sum'] =0
        if expense['amount__sum'] == None: expense['amount__sum'] =0
        if milk_production['total_milk__sum'] == None: milk_production['total_milk__sum'] =0
        income_data.append(income['amount__sum'])
        expense_data.append(expense['amount__sum'])
        milk_data.append(milk_production['total_milk__sum'])
    return JsonResponse(data={
        'labels': labels,
        'income_data': income_data,
        'expense_data':expense_data,
        'milk_data': milk_data
    })

"""Module Breeding"""
@login_required
def addBreeding(request):
    if request.method == 'POST':
        form = BreedingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Show_breeding')
    else:
        form = BreedingForm()
    return render(request,'Cow/add_breeding.html',{'form':form})

#display Breeding
@login_required
def showBreeding(request):
    if request.method == 'POST':
        result = request.POST['result']
        id = request.POST['id_value']
        breeding = Breeding.objects.get(id=id)
        breeding.result = result
        if result == "Successful":
            calf_due = breeding.date+datetime.timedelta(days=285)
            pregnant_cow = PregnantCow.objects.create(cow=breeding.cow,calf_due=calf_due)
            pregnant_cow.save()
        breeding.save()
        redirect('Show_breeding')
    start_date = request.GET.get('start_date')
    end_date =   request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            breedings = Breeding.objects.filter(date__range=[start_date,end_date])
        else:
            breedings = Breeding.objects.all()
    else:
        breedings = Breeding.objects.all()
    breeding_filter = BreedingFilter(request.GET,queryset=breedings)
    context = {
        'breeding_filter':breeding_filter,
    }
    return render(request,'Cow/show_breeding.html',context)
    

#update breeding 
@login_required
def breedingUpdate(request,id):
    breeding = Breeding.objects.get(id=id)
    select = ""
    if request.method == 'POST':
        if breeding.result != None:
            form = BreedingUpdateForm(request.POST,instance=breeding)
            select = "result"
        else:
            form = BreedingForm(request.POST,instance=breeding)
        if form.is_valid():
            if select == 'result':
                if form['result'].value() == 'Unsuccessful':
                    print("Iam herel")
                    if PregnantCow.objects.filter(cow=breeding.cow).exists():
                        PregnantCow.objects.get(cow=breeding.cow).delete()
                elif form['result'].value() == 'Successful':
                    if PregnantCow.objects.filter(cow=breeding.cow).exists() == False:
                        calf_due = breeding.date+datetime.timedelta(days=285)
                        pregnant_cow = PregnantCow.objects.create(cow=breeding.cow,calf_due=calf_due)
                        pregnant_cow.save()
            form.save()
            messages.success(request,"Breeding information updated successfully!")
            return redirect("Show_breeding")
    else:
        if breeding.result != None:
            form = BreedingUpdateForm(instance=breeding)
        else:
            form = BreedingForm(instance=breeding)
    return render(request,'Cow/add_breeding.html',{'form':form})

#Delete Breeding
@login_required
def breedingDelete(request,id):
    breeding = Breeding.objects.get(id=id)
    if PregnantCow.objects.filter(cow=breeding.cow).exists():
        messages.warning(request,"cannot delete this record!")
    else:
        breeding.delete()
        messages.success(request,"Breeding information deleted successfully!")
    return redirect('Show_breeding')



# Show Pregnant cow
@login_required
def showPregnantCow(request):
    context ={
        'pregnant_cow' : PregnantCow.objects.all(),
    }
    return render(request,'Cow/show_pregnant_cow.html',context)
    
#cow delivered
@login_required
def cowDelivered(request,id):
    pregnant_cow = PregnantCow.objects.get(id=id)
    cow = Cow.objects.filter(cow=pregnant_cow.cow)
    if cow.status == "Hiefer":
        cow.status = "Cow"
        cow.save()
    return redirect('Add_cow',cow="2")

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        context = {
        'cow_counts' : CowCount.objects.all(),
        'production_details' : ProductionDetail.objects.all(),
        'expense_details':ExpenseDetail.objects.all(),
        'cow_expense':CowExpenseDetail.objects.all(),
        'date':datetime.date.today()   
    }
        pdf = render_to_pdf('Cow/report_print.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Report_%s.pdf"%(context['date'])
            #download = request.GET.get('download')
            content = "inline; filename=%s " % (filename)
            response['Content-Disposition'] = content
            report_file = BytesIO(pdf.content)
            document = Document.objects.create(title=f"Report {datetime.date.today()}",file=File(report_file, filename),document_type='Monthly Report')
            document.save()
            return response
        else:
            return HttpResponse("Not found")

#Refresh
@login_required
def refresh(request):
    cows = Cow.objects.all()
    for cow in cows:
        if cow.dob != None:
            dob = cow.dob
            dif = datetime.date.today()-dob
            sum = dif.days
            
            years = math.floor(sum / 365);
            months = math.floor((sum - (years * 365))/30.5);
            days = (sum - (years * 365) - (months * 30.5))
           
            if cow.cow_age == None:
                age = Age.objects.create(year=years,month=months,day=days)
                age.save()
                cow.cow_age = age
            else:
                age = cow.cow_age
                age.day = days
                age.month = months
                age.year = years
                age.save()
            if cow.status == "Calf":
                if sum >= 274:
                    cow.status = "Hiefer"  
            cow.save()
            if cow.name == "Rahul":
                print("Days",cow.cow_age.day)  
        elif cow.is_brought == True:
            wb_days = cow.cow_age_when_brought.day
            wb_months = cow.cow_age_when_brought.month
            wb_years = cow.cow_age_when_brought.year
            all_days =(wb_years*365)+(wb_months*30.5)+wb_days  
            brought_date = cow.brought_date
            diff = datetime.date.today()-brought_date
            sum = diff.days + all_days
            years = math.floor(sum / 365);
            months = math.floor((sum - (years * 365))/30.5);
            days = (sum - (years * 365) - (months * 30.5))
            if cow.cow_age != None:
                age = cow.cow_age
                age.day = days
                age.month = months
                age.year = years
                age.save()
            else:
                age  = Age.objects.create(year=years,month=months,day=days)
                age.save()
                cow.cow_age = age
            if cow.status == "Calf":
                if sum >= 274:
                    cow.status = "Hiefer"
            cow.save()
        
    return redirect('Display_cow')    

#Inbox view
@login_required
def inbox(request):
    context = {
        'inbox':Inbox.objects.all().order_by('-date')
    }
    return render(request,'Cow/inbox.html',context)

#Message view
@login_required
def viewMessage(request,id):
    message = Inbox.objects.get(id=id)
    if message.seen == False:
        message.seen = True
        message.save()
    return render(request,'Cow/view-message.html',{'message':message})

#Print message
@login_required
def messagePrint(request,id):
    message = Inbox.objects.get(id=id)
    context = {
        'message':message
    }
    pdf = render_to_pdf('Cow/message-print.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Message_%s.pdf"%(message.name)
    
        content = "inline; filename=%s " % (filename)
        response['Content-Disposition'] = content 
        return response
    else:
        return HttpResponse("Not found")

#Delete message
@login_required
def messageDelete(request,id):
    message = Inbox.objects.get(id=id)
    message.delete()
    messages.success(request,'Message deleted successfully!')
    return redirect('Inbox')

#Donation adding
@login_required()
def addDonation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Donation information added succesfully!')
            return redirect('Show_donation')
    else:
        form = DonationForm()
    return render(request,'Cow/add_donation.html',{'form':form})

#Showo Donations
def showDonations(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date != None and end_date != None:
        if start_date != "" and end_date != "":
            start_date = datetime.datetime.strptime (start_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime('%Y-%m-%d')
            donations = Donation.objects.filter(date__range=[start_date,end_date])
        else:
            donations = Donation.objects.all().order_by('-date')
    else:
        donations = Donation.objects.all().order_by('-date')
    donation_filter = DonationFilter(request.GET,queryset=donations)
    return render(request,'Cow/show_donation.html',{'donation_filter':donation_filter})

#Update donations
def donationUpdate(request,id):
    donation = Donation.objects.get(id=id)
    if request.method == 'POST':
        form = DonationForm(request.POST,instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request,'Donation information updated successfully!')
            return redirect('Show_donation')
    else:
        form = DonationForm(instance=donation)
    return render(request,'Cow/add_donation.html',{'form':form})

#delete donations
def donationDelete(request,id):
    donation = Donation.objects.get(id=id)
    donation.delete()
    messages.success(request,'Donation information deleted successfully!')
    return redirect('Show_donation')


@login_required
def donationPrint(request,id):
    donation = Donation.objects.get(id=id)
    context = {
        'donar_name' : donation.donar_name,
        'amount' : donation.amount,
        'date':donation.date, 
    }
    pdf = render_to_pdf('Cow/donation_recipt.html',context)
    if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Donation%s_%s.pdf"%(context['donar_name'],context['date'])
            #download = request.GET.get('download')
            content = "inline; filename=%s " % (filename)
            # response['Content-Disposition'] = content
            # report_file = BytesIO(pdf.content)
            # document = Document.objects.create(title=f"Invoice {context['name']} {datetime.date.today()}",file=File(report_file, filename),document_type='Invoice')
            # document.save()
            #ProductSale.objects.all().delete()
            return response
    else:
        return HttpResponse("Not found")
#404 Error Page
def error_404(request,exception):
    return render(request,'Cow/error-404.html')
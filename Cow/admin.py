from django.contrib import admin
from .models import Income,Cow,Breeding, SoldCow,Supervisor,PregnantCow,Age,EmployeeSalary,Inbox,Expense,FeedEntry,EmpAttendance,Milk,Production

admin.site.register(Income)
admin.site.register(Cow)
admin.site.register(Breeding)
admin.site.register(Supervisor)
admin.site.register(PregnantCow)
admin.site.register(Age)
admin.site.register(EmployeeSalary)
admin.site.register(Inbox)
admin.site.register(Expense)
admin.site.register(FeedEntry)
admin.site.register(SoldCow)
admin.site.register(EmpAttendance)

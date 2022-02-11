from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import GeneratePdf
urlpatterns = [
    #Home page url
    path('', views.home,name="Home"),
    #DashBoard
    path('admin_dashboard/',views.adminDashBorad,name='Dashboard'),
    #admin urls
    path('admin_dashboard/add_admin/',views.addSupervisor,name='Add_admin'),
    path('admin_dashboard/admin/detail/<id>/',views.show_user,name='Show_user'),
    path('admin_dashboard/admin/list/',views.show_admin,name='Show_admin'),
    path('accounts/login/',views.admin_login,name="Admin_login"),
    path('admin_dashboard/admin/logout/',views.admin_logout,name="Admin_logout"),
    path('admin_dashboard/admin/profile/',views.admin_profile,name="Admin_profile"),

    path('admin_dashboard/admin/update/',views.adminUpdate,name="Admin_update"),
    path('admin_dashboard/admin/password/change/',views.change_password,name="Password_change"),
    #Forgot password urls
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'), 
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'), 
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'), 
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'), 
    #Employee Urls
    path('admin_dashboard/add_employee/',views.addEmployee,name='Add_emp'),
    path('admin_dashboard/display_employee/',views.displayEmp,name='Display_emp'),
    path('admin_dashboard/<id>/emp_profile/',views.empProfile,name="Emp_profile"),
    path('admin_dashboard/<id>/employee_update/',views.employeeUpdate,name="Employee_update"),
    path('admin_dashboard/<id>/employee_delete/',views.empDelete,name="Employee_delete"),
    #Employee Attendance Urls
    path('admin_dashboard/empployee/attendance/',views.reroute,name="Emp_attendance"),
    path('admin_dashboard/empployee/attendance/<date>/',views.empAttendance,name="Emp_attendance1"),
    path('admin_dashboard/employee/attendance/add/<id>/',views.addAttendance,name="Add_attendance"),
    path('admin_dashboard/employee/attendance/list/',views.attendanceList,name="Emp_attendance_list"),
    path('admin_dashboard/employee/attendance/monthly/list/',views.monthlyAttendance,name="Emp_montly_attendance"),
    path('admin_dashboard/employee/attendance/update/<id>/',views.attendanceUpdate,name="Emp_attendance_update"),
    #Employee salary
    path('admin_dashboard/employee/salary/',views.empSalaryGenerate,name="Employee_salary"),
    path('admin_dashboard/employee/salary/<start_date>/<end_date>/',views.empSalaryDetail,name="Employee_salary_detail"),
    path('admin_dashboard/employee/salary/unpaid/',views.unpaid,name="Employee_salary_unpaid"),
    path('admin_dashboard/employee/salary/pay/',views.empSalaryPay,name="Employee_salary_pay"),
    path('admin_dashboard/employee/salary/delete/<start_date>/<end_date>/',views.salaryDelete,name="Delete_salary"),
    #Cow Urls
    path('admin_dashboard/cow/add_/<str:cow>/', views.addCow,name="Add_cow"),
    path('admin_dashboard/cow/list/',views.displayCow,name='Display_cow'),
    path('admin_dashboard/cow/delete/<id>/',views.cowDelete,name="Cow_delete"),
    path('admin_dashboard/cow/details/<id>/',views.cowDetails,name="Cow_details"),
    path('admin_dashboard/cow/details-by-name/<name>/',views.cowDetailsByName,name="Cow_details_by_name"),
    path('admin_dashboard/cow/update/<id>/',views.cowUpdate,name="Cow_update"),
    #Cow sale Urls
    path('admin_dashboard/cow/sale/add/',views.addSoldCow,name="Add_sold_cow"),
    path('admin_dashboard/cow/sale/list/',views.showSoldCow,name="Show_sold_cow"),
    path('admin_dashboard/cow/sale/delete/<id>/',views.soldCowDelete,name="Delete_sold_cow"),
    path('admin_dashboard/cow/sale/update/<id>/',views.soldCowUpdate,name="Update_sold_cow"),
    path('admin_dashboard/cow/sale/returned/<id>/',views.soldCowReturn,name="Return_sold_cow"),
    #Cow Health Urls
    path('admin_dashboard/cow/health/add/',views.addCowHealthRecord,name="Cow_health_record_add"),
    path('admin_dashboard/cow/health/list/',views.cowHealthRecordList,name="Cow_health_record_list"),
    path('admin_dashboard/cow/health/details/<id>/',views.cowHealthDetail,name="Cow_health_details"),
    path('admin_dashboard/cow/health/update/<id>/',views.cowHealthUpdate,name="Cow_health_update"),
    path('admin_dashboard/cow/health/delete/<id>/',views.cowHealthDelete,name="Cow_health_delete"),
    #Dead Cow Urls
    path('admin_dashboard/cow/death/add/',views.addDeadCow,name="Add_dead_cow"),
    path('admin_dashboard/cow/death/list/',views.showDeadCow,name="Show_dead_cow"),
    path('admin_dashboard/cow/death/update/<id>/',views.deadCowUpdate,name="Update_dead_cow"),
    path('admin_dashboard/cow/death/delete/<id>/',views.deadCowDelete,name="Delete_dead_cow"),
    #Cow Breed
    path('admin_dashboard/breeds/add/',views.addBreed,name="Add_breed"),
    path('admin_dashboard/breeds/add-ajax/',views.addBreedAjax,name="Add_breed_ajax"),
    path('admin_dashboard/breeds/list/',views.breedList,name="Display_breed"),
    path('admin_dashboard/breeds/update/<id>/',views.breedUpdate,name="Update_breed"),
    path('admin_dashboard/breeds/delete/<id>/',views.breedDelete,name="Delete_breed"),
    #Product urls
    path('admin_dashboard/products/add/',views.addProduct,name="Add_product"),
    path('admin_dashboard/products/list/',views.showProducts,name="Show_product"),
    path('admin_dashboard/products/upadte/<id>/',views.productsUpdate,name="Update_product"),
    path('admin_dashboard/products/delete/<id>/',views.productsDelete,name="Delete_product"),
    #Production Urls
    path('admin_dashboard/production/add/',views.addProduction,name="Add_production"),
    path('admin_dashboard/production/list/',views.showProduction,name="Show_production"),
    path('admin_dashboard/production/delete/<id>/',views.productionDelete,name="Delete_production"),
    path('admin_dashboard/production/update/<id>/',views.productionUpdate,name="Update_production"),
    #Product Usage Url
    path('admin_dashboard/products/usage/add/',views.addProductUse,name="Add_product_use"),
    path('admin_dashboard/products/usage/list/',views.showProductUse,name="Show_product_use"),
    path('admin_dashboard/products/usage/update/<id>/',views.productUseUpdate,name="Update_product_use"),
    path('admin_dashboard/products/usage/delete/<id>/',views.productUseDelete,name="Delete_product_use"),
    #Product sale Url
    path('admin_dashboard/products/sale/cart/',views.productCart,name="Product_cart"),
    path('admin_dashboard/products/sale/cart/delete/<id>/',views.cartProductDelete,name="Delete_product_cart"),
    path('admin_dashboard/products/sale/cart/all-delete/',views.allCartProductDelete,name="All_delete_product_cart"),
    path('admin_dashboard/products/sale/cart/update/<id>/',views.cartProductUpdate,name="Update_product_cart"),
    path('admin_dashboard/products/sale/billing/',views.billing,name="Billing"),
    path('admin_dashboard/products/sale/<option>/',views.addCartProduct,name="Product_sale"), 
    #Income Urls
    path('admin_dashboard/income/add/',views.addIncome,name="Add_income"),
    path('admin_dashboard/income/list/',views.showIncome,name="Show_income"),
    path('admin_dashboard/income/update/<id>/',views.incomeUpdate,name="Update_income"),
    path('admin_dashboard/income/delete/<id>/',views.incomeDelete,name="Delete_income"),
    #Expense Urls
    path('admin_dashboard/expense/add/',views.addExpenes,name="Add_expense"),
    path('admin_dashboard/expense/list/',views.showExpense,name="Show_expense"),
    path('admin_dashboard/expense/update/<id>/',views.expenseUpdate,name="Update_expense"),
    path('admin_dashboard/expense/delete/<id>/',views.expenseDelete,name="Delete_expense"),
    #Milk Urls
    path('admin_dashboard/milk/add/',views.addMilk,name="Add_milk"),
    path('admin_dashboard/milk/list/',views.showMilk,name="Show_milk"),
    path('admin_dashboard/milk/update/<id>/',views.milkUpdate,name="Update_milk"),
    path('admin_dashboard/milk/delete/<id>/',views.milkDelete,name="Delete_milk"),
    #Feed Feed urls
    path('admin_dashboard/feed/add',views.addFeedInfo,name="Add_feed_info"),
    path('admin_dashboard/feed/list/',views.showFeed,name="Feed_list"),
    path('admin_dashboard/feed/delete/<id>/',views.feedDelete,name="Feed_delete"),
    path('admin_dashboard/feed/update/<id>/',views.feedUpdate,name="Feed_update"),
    #Feed Supplier Urls
    path('admin_dashboard/feed/supplier/add/',views.addFeedSupplier,name="Add_feed_supplier"),
    path('admin_dashboard/feed/supplier/list/',views.showFeedSupplier,name="Supplier_list"),
    path('admin_dashboard/feed/supplier/update/<id>/',views.feedSupplierUpdate,name="Supplier_update"),
    path('admin_dashboard/feed/supplier/delete/<id>/',views.feedSupplierDelete,name="Supplier_delete"),
    #Feed Stock Entry Urls
    path('admin_dashboard/feed/stock-entry/add/',views.addFeedStockEntry,name="Add_feed_stock_entry"),
    path('admin_dashboard/feed/stock-entry/list/',views.showFeedEntry,name="Feed_stock_entry_list"),
    path('admin_dashboard/feed/stock-entry/update/<id>/',views.feedEntryUpdate,name="Feed_stock_entry_update"),
    path('admin_dashboard/feed/stock-entry/delete/<id>/',views.feedEntryDelete,name="Feed_stock_entry_delete"),
    #Feed Daily Usage Urls
    path('admin_dashboard/feed/usage/add/',views.addDailyFeedUsage,name="Add_feed_usage"),
    path('admin_dashboard/feed/usage/list/',views.showFeedUsage,name="Show_feed_usage"),
    path('admin_dashboard/feed/usage/delete/<id>/',views.feedUsageDelete,name="Delete_feed_usage"),
    path('admin_dashboard/feed/usage/update/<id>/',views.feedUsageUpdate,name="Update_feed_usage"),
    #Maothly Report 
    path('admin_dashboard/report/',views.monthlyRecord,name="Show_month_report"),
    #Print Url
    path('admin_dashboard/report/print/<option>/',views.printPage,name="Print_page"),
    #Assets Urls
    path('admin_dashboard/asset/add/',views.addAssets,name="Add_asset"),
    path('admin_dashboard/asset/list/',views.showAssets,name="Show_asset"),
    path('admin_dashboard/asset/update/<id>/',views.assetUpdate,name="Update_asset"),
    path('admin_dashboard/asset/delete/<id>/',views.assetDelete,name="Delete_asset"),
    #Document Urls
    path('admin_dashboard/document/add/',views.addDocuments,name="Add_document"),
    path('admin_dashboard/document/list/',views.showDocuments,name="Show_document"),
    path('admin_dashboard/document/update/<id>/',views.documentUpdate,name="Update_document"),
    path('admin_dashboard/document/delete/<id>/',views.documentDelete,name="Delete_document"),
    #Chart Urls
    #path('expense-chart/', views.expense_chart, name='expense-chart'),
    path('income-chart/', views.income_chart, name='income-chart'),
    #Breeding Urls
    path('admin_dashboard/breeding/add/',views.addBreeding,name="Add_breeding"),
    path('admin_dashboard/breeding/list/',views.showBreeding,name="Show_breeding"),
    path('admin_dashboard/breeding/update/<id>/',views.breedingUpdate,name="Update_breeding"),
    path('admin_dashboard/breeding/delete/<id>/',views.breedingDelete,name="Delete_breeding"),
    #Pregnant Cow url
    path('admin_dashboard/pregnant-cow/list/',views.showPregnantCow,name="Show_pregnant_cow"),
    path('admin_dashboard/pregnant-cow/delivered/<id>/',views.cowDelivered,name="Cow_delivered"),

    #Refresh Urls
    path('admin_dashboard/refresh/',views.refresh,name="Refresh"),
    path('admin_dashboard/pdf/', GeneratePdf.as_view()), 
    #Inbox url
    path('admin_dashboard/inbox/',views.inbox,name="Inbox"),
    path('admin_dashboard/inbox/view-message/<id>/',views.viewMessage,name="View_message"),
    path('admin_dashboard/inbox/view-message/print/<id>/',views.messagePrint,name="Print_message"),
    path('admin_dashboard/inbox/delete-message/<id>/',views.messageDelete,name="Delete_message"),
    #Donations Urls
    path('admin_dashboard/donation/add/',views.addDonation,name="Add_donation"),
    path('admin_dashboard/donation/list/',views.showDonations,name="Show_donation"),
    path('admin_dashboard/donation/update/<id>/',views.donationUpdate,name="Update_donation"),
    path('admin_dashboard/donation/delete/<id>/',views.donationDelete,name="Delete_donation"),
    path('admin_dashboard/donation/print/<id>/',views.donationPrint,name="Print_donation"),



]
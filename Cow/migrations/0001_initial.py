# Generated by Django 3.2.6 on 2021-08-16 05:04

import Cow.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_name', models.CharField(max_length=30)),
                ('asset_id', models.CharField(max_length=20, unique=True)),
                ('purchase_date', models.DateField()),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('about', models.TextField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('tag_number', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('age', models.IntegerField(blank=True, max_length=3, null=True)),
                ('age_duration_type', models.CharField(blank=True, choices=[('Day', 'Day'), ('Month', 'Month'), ('Year', 'Year')], max_length=6, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('mother', models.CharField(blank=True, max_length=30, null=True)),
                ('father', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.CharField(choices=[('', 'Select a status'), ('Karu', 'Karu'), ('Hori', 'Hori'), ('Gadasu', 'Gadasu'), ('Aakalu', 'Aakalu')], max_length=30)),
                ('brought_from', models.CharField(blank=True, max_length=50, null=True)),
                ('brought_date', models.DateField(blank=True, null=True)),
                ('age_when_brought', models.IntegerField(blank=True, max_length=3, null=True)),
                ('is_dead', models.BooleanField(default=False)),
                ('is_brought', models.BooleanField(default=False)),
                ('is_sold', models.BooleanField(default=False)),
                ('breed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Cow.breed')),
            ],
        ),
        migrations.CreateModel(
            name='CowExpenseDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cow', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('month_expense', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('one_cow_day_expense', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('all_cow_day_expense', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('one_cow_month_expense', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
            ],
            options={
                'verbose_name': 'CowExpenseDetail',
                'verbose_name_plural': 'CowExpenseDetails',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('document_type', models.CharField(choices=[('cow', 'Cow'), ('employee', 'Employee'), ('monthly_record', 'Monthly Records'), ('other', 'Other')], max_length=15)),
                ('file', models.FileField(upload_to=Cow.models.content_file_name)),
                ('add_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=10)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('home', models.CharField(max_length=30)),
                ('village', models.CharField(max_length=30)),
                ('aadhaar_no', models.CharField(blank=True, max_length=12, null=True)),
                ('bank_account_no', models.CharField(blank=True, max_length=12, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('join_date', models.DateField(blank=True, null=True)),
                ('profile_pic', models.FileField(blank=True, null=True, upload_to='images/')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(choices=[('ona_hullu', 'Ona Hullu'), ('hindi', 'Hindi'), ('haale_hudi', 'Haale Hudi'), ('medicine', 'Medicine'), ('salary', 'Salary'), ('current_bill', 'Current Bill'), ('newpapaer_bill', 'NewsPaper Bill'), ('repair_maintainance', 'Repair & Maintainance'), ('food', 'Food'), ('transport', 'Transport'), ('other', 'Other')], max_length=30)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('unit', models.CharField(blank=True, choices=[('Kg', 'KG'), ('Litre', 'Litre'), ('Bundle', 'Bundle'), ('KM', 'KM'), ('Box', 'Box'), ('Bag', 'Bag'), ('Packet', 'Packets'), ('--', 'Other')], max_length=30, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=30)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
            ],
            options={
                'verbose_name': 'ExpenseDetail',
                'verbose_name_plural': 'ExpenseDetails',
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
                ('stock', models.DecimalField(decimal_places=2, max_digits=7)),
                ('about', models.TextField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Feed',
                'verbose_name_plural': 'Feeds',
            },
        ),
        migrations.CreateModel(
            name='FeedSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('address', models.TextField(max_length=100)),
                ('phone', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=254)),
                ('GST_no', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Milk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('session', models.CharField(choices=[('Morning', 'Morning'), ('Evening', 'Evening')], max_length=10)),
                ('calf_use', models.DecimalField(decimal_places=2, max_digits=5)),
                ('employee_use', models.DecimalField(decimal_places=2, max_digits=5)),
                ('local_sale', models.DecimalField(decimal_places=2, max_digits=5)),
                ('local_sale_income', models.DecimalField(decimal_places=2, max_digits=5)),
                ('dairy_sale', models.DecimalField(decimal_places=2, max_digits=5)),
                ('dairy_sale_income', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total_milk', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total_income', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('unit', models.CharField(choices=[('Kg', 'KG'), ('Litre', 'Litre'), ('Bundle', 'Bundle'), ('KM', 'KM'), ('Box', 'Box'), ('Bag', 'Bag'), ('Packet', 'Packets'), ('--', 'Other')], max_length=30)),
                ('stock', models.DecimalField(decimal_places=2, max_digits=8)),
                ('about', models.TextField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=6)),
                ('profile_pic', models.FileField(blank=True, null=True, upload_to='images/')),
                ('date_of_join', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SoldCow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sold_to', models.CharField(max_length=30)),
                ('sold_address', models.TextField(max_length=100)),
                ('sold_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('returned', models.BooleanField(default=False)),
                ('cow', models.ForeignKey(default='Deleted Cow', on_delete=django.db.models.deletion.SET_DEFAULT, to='Cow.cow')),
            ],
        ),
        migrations.CreateModel(
            name='ProductUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(default='Deleted Product', on_delete=django.db.models.deletion.SET_DEFAULT, to='Cow.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hsn', models.CharField(max_length=15)),
                ('unit', models.DecimalField(decimal_places=2, max_digits=8)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=8)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cgst', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('sgst', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('igst', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cow.product')),
            ],
            options={
                'verbose_name': 'ProductSale',
                'verbose_name_plural': 'ProductSales',
            },
        ),
        migrations.CreateModel(
            name='ProductionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('production_quantity', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('sale_quantity', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('sale_amount', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('self_use', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('calf_use', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('remaining', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('product', models.ForeignKey(default='Deleted Product', on_delete=django.db.models.deletion.SET_DEFAULT, to='Cow.product')),
            ],
            options={
                'verbose_name': 'ProductionDetail',
                'verbose_name_plural': 'ProductionDetails',
            },
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cow.product')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cow.product')),
            ],
        ),
        migrations.CreateModel(
            name='FeedEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('bags', models.DecimalField(decimal_places=2, max_digits=6)),
                ('bag_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('feed_rate', models.DecimalField(decimal_places=2, max_digits=6)),
                ('payment', models.DecimalField(decimal_places=2, max_digits=8)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cow.feed')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cow.feedsupplier')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('attendance', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('payable_salary', models.FloatField(null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('paid_on', models.DateField(blank=True, null=True)),
                ('employee', models.ForeignKey(default='Deleted Employee', on_delete=django.db.models.deletion.SET_DEFAULT, to='Cow.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmpAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField(default=django.utils.timezone.now)),
                ('attendance', models.CharField(choices=[('half', 'Half Day'), ('full', 'Full Day'), ('leave', 'Leave')], max_length=8)),
                ('is_added', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cow.employee')),
            ],
        ),
        migrations.CreateModel(
            name='DeadCow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cause_of_death', models.CharField(choices=[('Normal', 'Normal'), ('Disease', 'Disease'), ('Accident', 'Accident'), ('Other', 'Other')], max_length=20)),
                ('date', models.DateField(verbose_name=django.utils.timezone.now)),
                ('cow', models.ForeignKey(default='Deleted Cow', on_delete=django.db.models.deletion.SET_DEFAULT, to='Cow.cow')),
            ],
        ),
        migrations.CreateModel(
            name='DailyFeedUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('feed', models.ForeignKey(default='Deleted Feed', on_delete=django.db.models.deletion.SET_DEFAULT, to='Cow.feed')),
            ],
        ),
        migrations.CreateModel(
            name='CowHealth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('cured_date', models.DateField(blank=True, null=True)),
                ('doctor', models.CharField(blank=True, max_length=50, null=True)),
                ('medicine', models.CharField(blank=True, max_length=100, null=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cow.cow')),
            ],
        ),
        migrations.CreateModel(
            name='CowCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('akalu_count', models.IntegerField()),
                ('gadasu_count', models.IntegerField()),
                ('hori_count', models.IntegerField()),
                ('male_calf_count', models.IntegerField()),
                ('female_calf_count', models.IntegerField()),
                ('sold_cow_count', models.IntegerField()),
                ('dead_cow_count', models.IntegerField()),
                ('total_count', models.IntegerField()),
                ('breed', models.ForeignKey(default='Deleted Breeed', on_delete=django.db.models.deletion.SET_DEFAULT, to='Cow.breed')),
            ],
            options={
                'verbose_name': 'CowCount',
                'verbose_name_plural': 'CowCounts',
            },
        ),
    ]

import datetime
from .models import Income, Product
def my_scheduled_job():
    product = Product.objects.get(title="Cow")
    income = Income.objects.create(product=product,quantity=1,date=datetime.date.today(),amount=100)
    income.save()
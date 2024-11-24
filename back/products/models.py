# products/models.py
from django.db import models

class Product(models.Model):
    PRODUCT_TYPES = (
        ('deposit', '예금'),
        ('savings', '적금'),
    )
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES)
    dcls_month = models.CharField(max_length=6)
    fin_prdt_cd = models.TextField(unique=True)
    fin_prdt_nm = models.TextField()
    kor_co_nm = models.TextField()
    etc_note = models.TextField()
    join_deny = models.IntegerField()
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()

# products/models.py
class Option(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    dcls_month = models.CharField(max_length=6)
    intr_rate_type_nm = models.CharField(max_length=100)
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    save_trm = models.IntegerField()  # 추가

class ProductMark(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

class ProductComment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
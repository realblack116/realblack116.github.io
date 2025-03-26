from django.db import models
from products.models import Product

class Order(models.Model):
    name = models.CharField(max_length=100)  # 사용자 이름
    email = models.EmailField()              # 이메일
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title}"

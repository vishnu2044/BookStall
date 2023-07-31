from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.
def validate_expiry_date(value):
    min_date = date.today()
    if value < min_date:
        raise ValidationError(
            (f"Expiry date cannot be earlier than {min_date}.")
        )
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=15)
    min_amount = models.PositiveBigIntegerField()
    off_percent = models.PositiveBigIntegerField()
    max_discount = models.PositiveBigIntegerField()
    coupon_stock = models.PositiveIntegerField(null=True, blank=True)
    expiry_date = models.DateField(validators=[validate_expiry_date])

    def str(self):
        return self.coupon_code
    
    def is_expired(self):
        if self.coupon_stock == 0 or self.expiry_date < date.today():
            return True
        return False


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    '''Model to store coupons.
    
    Properties:
        code: Code to be entered by the users in order to apply the coupon to their service.
        valid_from: Datetime value indicating when the coupon becomes valid.
        valid_to: Datetime value indicating when the coupon becomes invalid.
        discount: Discount rate to apply (percentage). Validators are in place to limit the min and max.
        active: Boolean indicating whether the coupon is active.
    '''
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code

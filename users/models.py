from django.db import models

# Create your models here.
class Userregistration(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=500)
    role = models.CharField(max_length=20)
    
    def register(self):
        self.save()

    def __str__(self):
        return (self.email)
    @staticmethod
    def get_customer_by_email(email):
        return Userregistration.objects.get(email = email)

    def isExists(self):
        if Userregistration.objects.filter(email = self.email):
            return True
        else:
            return False


class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    quantity= models.IntegerField(default=0)
    choices = (('Active', "Active"),('Inactive', "Inactive"))
    status= models.CharField(max_length=8 , choices=choices, default="Active")
    image = models.ImageField(upload_to='products/')

    def reg(self):
        self.save()

    def __str__(self):
        return (self.name)
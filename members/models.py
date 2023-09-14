from django.db import models

class User(models.Model):
    uid = models.AutoField(primary_key=True)  # AutoField for the UID
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=255)  # You can adjust the max_length as needed
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Car(models.Model):
    vno = models.AutoField(primary_key=True)
    model = models.CharField(max_length=20, unique=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    nos = models.PositiveSmallIntegerField(default=4)
    occup = models.BooleanField(default=False)

    def __str__(self):
        return self.model

class Rent(models.Model):
    rid = models.AutoField(primary_key=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    given = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nod = models.PositiveSmallIntegerField(default=1)
    start = models.DateField()
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    vno = models.ForeignKey(Car, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Rent {self.rid}"

        
class Payment(models.Model):
    pid = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)  
    dat = models.DateField()
    rid = models.ForeignKey(Rent, on_delete=models.CASCADE)  

    def __str__(self):
        return f"Payment {self.pid}"








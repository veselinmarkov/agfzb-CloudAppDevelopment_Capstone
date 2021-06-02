from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(null=False, max_length=45, default='Audi')
    description = models.CharField(null=True, max_length=1000)
    def __str__(self):
        return 'Car make:' +self.name +' description:' +self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]
    id = models.IntegerField(primary_key=True, null=False)
    carmake = models.ForeignKey(to=CarMake, on_delete=models.CASCADE)   
    name = models.CharField(null=False, max_length=45, default='A6')
    dealer = models.IntegerField(null=True)
    cartype = models.CharField(max_length=45, choices=TYPE_CHOICES, default=SEDAN)
    year = models.DateField(null=True)
    def __str__(self):
        return 'Car model:' +self.name +' ' +self.carmake.name +' ' +self.cartype +\
        ' dealer:' +str(self.dealer) +' year:'+str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(dict):
    pass

# <HINT> Create a plain Python class `DealerReview` to hold review data

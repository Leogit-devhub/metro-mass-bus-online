from django.db import models


class Town(models.Model):
  name = models.CharField(max_length=120)
  desc = models.TextField(null=True, blank=True)
  date = models.DateTimeField(auto_now_add = True)
  
  def __str__(self):
    return self.name


class Route(models.Model):
  origin = models.ForeignKey(Town, related_name="route_from", on_delete=models.CASCADE, null=True, blank=True)
  to = models.ForeignKey(Town, related_name="route_to", on_delete=models.CASCADE, null=True, blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  date = models.DateTimeField(auto_now_add = True)
  
  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['origin', 'to'], name='unique route')
    ]
  
  def __str__(self):
    return f"{self.origin} - {self.to}"


class BookBy(models.Model):
  name = models.CharField(max_length=120)
  contact = models.CharField(max_length=120)
  address = models.TextField(max_length=120)
  
  def __str__(self):
      return self.name

  
class PassengerInfo(models.Model):
  Gender = (
    ('m', 'Male'),
    ('f', 'Female'),
  )
  
  route = models.ForeignKey(Route, related_name="ticket_route", on_delete=models.CASCADE, null=True, blank=True)
  
  name = models.CharField(max_length=120)
  
  age = models.SmallIntegerField()
  
  contact = models.CharField(max_length=13)
  
  gender = models.CharField(choices=Gender, max_length=120, null=True, blank=True)

  seat = models.SmallIntegerField(null=True, blank=True)
  
  date = models.DateTimeField(auto_now_add = True)
  
  def __str__(self):
    return self.name
  
  def get_price(self):
    return self.route.price

from django.db import models


class Town(models.Model):
  name = models.CharField(max_length=120, help_text = "Name of the town ! Required.")
  desc = models.TextField(null=True, blank=True, help_text = "Bus stops or any ! Not Required.")
  date = models.DateTimeField(auto_now_add = True)
  
  def __str__(self):
    return self.name


class Route(models.Model):
  origin = models.ForeignKey(Town, related_name="route_from", on_delete=models.CASCADE)
  to = models.ForeignKey(Town, related_name="route_to", on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  date = models.DateTimeField(auto_now_add = True)
  
  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['origin', 'to'], name='unique route')
    ]
  
  def __str__(self):
    return f"{self.origin} - {self.to}"

class Session(models.Model):
  description = models.CharField(max_length=120, help_text = "Early Morning / Morning / Mid-Day / Evening / etc")
  time = models.TimeField(help_text = "HH:MM:SS")
  
  def __str__(self):
    return f"{self.description} - {self.time}"


class BookBy(models.Model):
  name = models.CharField(max_length=120)
  contact = models.CharField(max_length=120)
  address = models.TextField(max_length=120)
  
  def __str__(self):
      return self.name


class Buse(models.Model):
  driver_name = models.CharField(max_length=120)
  driver_contact = models.CharField(max_length=13)
  bus_number = models.CharField(max_length=50,)
  seats = models.SmallIntegerField(help_text = "Number of seats/passenger this bus can take")
  route = models.ForeignKey(Route, related_name="bus_route", on_delete=models.CASCADE)
  session = models.ForeignKey(Session, related_name="bus_session", on_delete=models.CASCADE)
  d_date = models.DateField(max_length=120)
  date = models.DateTimeField(auto_now=False, auto_now_add=False)
    
  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['bus_number', 'd_date'], name='unique bus_number')
    ]
  
  def __str__(self):
    return self.bus_number
  
  def bus_full(self, new_pass_count):
    p_count = 0
    booked = self.reservation_bus.all()
    for reserved in booked:
      p_count += reserved.passengers_count()
    if (p_count + int(new_pass_count)) <= self.seats:
      return True
    return False

 
class PassengerInfo(models.Model):
  Gender = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Others'),
  )
  
  route = models.ForeignKey(Route, related_name="ticket_route", on_delete=models.CASCADE)
  
  name = models.CharField(max_length=120)
  
  age = models.SmallIntegerField()
  
  contact = models.CharField(max_length=13)
  
  gender = models.CharField(choices=Gender, max_length=120)

  seat = models.SmallIntegerField()
  
  date = models.DateTimeField(auto_now_add = True)
  
  def __str__(self):
    return self.name
  
  def get_price(self):
    return self.route.price


class UserMessage(models.Model):
  name = models.CharField(("Full Name"), max_length=60)
  phone = models.CharField(("Phone Number"), max_length=13)
  email = models.EmailField(("Email"), max_length=120, null=True, blank=True, help_text="Not Required !")
  purpose = models.CharField(("Main Purpose / Issue"), max_length=120)
  details = models.TextField()
  date = models.DateField(auto_now=False, auto_now_add=True)
  
  def __str__(self):
    return self.purpose
  
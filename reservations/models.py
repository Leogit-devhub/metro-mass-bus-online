from django.db import models
from django.urls import reverse

from utils.models import BookBy, Buse, PassengerInfo, Route, Session

class Reservation(models.Model):
  book_by = models.ForeignKey(BookBy, related_name="book_by", on_delete=models.CASCADE, help_text = "Clik on 'plus' button to add a new 'book by'.")
  passengers = models.ManyToManyField(PassengerInfo, related_name="passenger", null=True, blank=True, help_text = "Click on the 'plus' button to add a passenger !")
  bus = models.ForeignKey(Buse, related_name="reservation_bus", on_delete=models.CASCADE)
  session = models.ForeignKey(Session, related_name="reservation_session", on_delete=models.CASCADE)
  d_date = models.DateField(max_length=120)
  date_created = models.DateTimeField(auto_now_add = True)
  approved = models.BooleanField(default=False)

  def __str__(self):
    return self.book_by.name

  def passengers_count(self):
    return self.passengers.all().count()
    
  def get_absolute_url(self):
    return reverse("book_details", kwargs={"pk": self.pk})
  
  def get_print_url(self):
    return reverse("book_print", kwargs={"pk": self.pk})

  def get_total_price(self):
    prices = []
    for passenger in self.passengers.all():
      prices.append(passenger.route.price)
    return sum(prices)
  
  def get_route(self):
    return self.passengers.first().route


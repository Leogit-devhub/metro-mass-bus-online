from django.contrib import admin

from .models import BookBy, Discount, Town, Route, PassengerInfo


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
  pass

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
  list_display = ("origin", "to", "price")
  
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
  pass

@admin.register(BookBy)
class BookByAdmin(admin.ModelAdmin):
  list_display = ("name", "contact", "contact")

@admin.register(PassengerInfo)
class PassengerInfoAdmin(admin.ModelAdmin):
  list_display = ("name", "age", "contact", "seat", "discount", "route")

from django.contrib import admin

from .models import BookBy, Buse, Session, Town, Route, PassengerInfo, UserMessage


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
  pass

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
  list_display = ("origin", "to", "price")
  
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
  list_display = ("description", "time")
  
@admin.register(Buse)
class BuseAdmin(admin.ModelAdmin):
  list_display = ("bus_number", "driver_name", "driver_contact", "seats", "route", "session", "d_date")

@admin.register(BookBy)
class BookByAdmin(admin.ModelAdmin):
  list_display = ("name", "contact", "contact")

@admin.register(PassengerInfo)
class PassengerInfoAdmin(admin.ModelAdmin):
  list_display = ("name", "age", "contact", "seat", "route")

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
  list_display = ("purpose", "name", "phone", "email")

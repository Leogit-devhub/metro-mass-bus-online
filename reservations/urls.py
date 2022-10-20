from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('init_reservation/', views.ReservationInitialView.as_view(), name='reservation_init'),
    path('reservation/?', views.ReservationView.as_view(), name='reservation_form'),
    path('book/<str:pk>/details/', views.ReservationDetailsView.as_view(), name='book_details'),
    path('passenger/<str:pk>/delete/',  views.DeletePassenger.as_view(), name='delete_passenger'),
    path('reservation/<str:pk>/delete/',  views.DeleteReservation.as_view(), name='delete_reservation'),
]

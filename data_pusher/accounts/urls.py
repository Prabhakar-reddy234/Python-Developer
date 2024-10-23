from django.urls import path
from .views import AccountListCreateView, AccountDetailView, DestinationListCreateView, DestinationDetailView, IncomingDataHandler

urlpatterns = [
    # Account URLs
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('accounts/<uuid:pk>/', AccountDetailView.as_view(), name='account-detail'),

    # Destination URLs
    path('destinations/', DestinationListCreateView.as_view(), name='destination-list-create'),
    path('destinations/<int:pk>/', DestinationDetailView.as_view(), name='destination-detail'),

    # Data handler URL
    path('server/incoming_data/', IncomingDataHandler.as_view(), name='incoming-data'),
]

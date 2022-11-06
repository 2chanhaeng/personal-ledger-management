from django.urls import path
from . import views

urlpatterns = [
    path("", views.LedgersView.as_view()),
    path("<ledger_id>/", views.LedgerDetailView.as_view()),
]

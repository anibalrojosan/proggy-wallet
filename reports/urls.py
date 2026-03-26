from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("export/transactions.csv", views.TransactionCsvExportView.as_view(), name="export_transactions_csv"),
]

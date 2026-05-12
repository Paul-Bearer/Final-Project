from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_case", views.add_case, name="add_case"),
    path("edit_case/<int:deceased_id>/", views.edit_case, name="edit_case"),
    path("save_deceased_info/<int:deceased_id>/", views.save_deceased_info, name="save_deceased_info"),
    path("save_obituary/<int:deceased_id>/", views.save_obituary, name="save_obituary"),
    path("add_event/<int:deceased_id>/", views.add_event, name="add_event"),
    path("delete_event/<int:event_id>/", views.delete_event, name="delete_event"),
    path("edit_event/<int:event_id>/", views.edit_event, name="edit_event"),
    path("save_finance/<int:deceased_id>/", views.save_finance, name="save_finance"),
    path("delete_product/<int:product_id>", views.delete_product, name="delete_product"),
    path("edit_product/<int:product_id>", views.edit_product, name="edit_product")

]
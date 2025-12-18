from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('attendance_list/', attendance_list, name='attendance_list'),
    path('attendance/create/', attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/edit/', attendance_edit, name='attendance_edit'),
    path('attendance/<int:pk>/delete/', attendance_delete, name='attendance_delete'),
    path('shift_list/', shift_list, name='shift_list'),
    path('leave_request_list/', leave_request_list, name='leave_request_list'),
    path('holiday_list/', holiday_list, name='holiday_list'),
    path('holiday/create/', holiday_create, name='holiday_create'),
    path('holiday/<int:pk>/edit/', holiday_edit, name='holiday_edit'),
    path('holiday/<int:pk>/delete/', holiday_delete, name='holiday_delete'),
    path("leave/create/", leave_create, name="leave-create"),
    # path("leave/", leave_list, name="leave-list"),

]

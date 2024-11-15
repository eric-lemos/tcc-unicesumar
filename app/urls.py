from django.urls import path
from . import views

urlpatterns = [
    # Login
    path('', views.redirect_login, name='redirect_login'),
    path('login/', views.login, name='login'),
    path("logout/", views.logout, name="logout"),
    path('login/register', views.register, name='register'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/error', views.notfound, name='error'),

    # Profile
    path('dashboard/profile', views.profile, name='profile'),

    # Calendar
    path('dashboard/calendar', views.calendar, name='calendar'),
    path('dashboard/calendar/add', views.add_calendar, name='add_calendar'),
    path('dashboard/calendar/get/<int:pk>', views.get_calendar, name='get_calendar'),
    path('dashboard/calendar/edit/<int:pk>', views.edit_calendar, name='edit_calendar'),
    path('dashboard/calendar/approve/<int:pk>', views.approve_calendar, name='approve_calendar'),
    path('dashboard/calendar/cancel/<int:pk>', views.cancel_calendar, name='cancel_calendar'),
    path('dashboard/calendar/away/<int:pk>', views.away_calendar, name='away_calendar'),
    path('dashboard/calendar/done/<int:pk>', views.done_calendar, name='done_calendar'),

    # Managers
    path('dashboard/managers', views.managers, name='managers'),
    path('dashboard/managers/add', views.add_manager, name='add_manager'),
    path('dashboard/managers/get/<int:pk>', views.get_manager, name='get_manager'),
    path('dashboard/managers/del/<int:pk>', views.del_manager, name='del_manager'),
    path('dashboard/managers/edit/<int:pk>', views.edit_manager, name='edit_manager'),

    # Doctors
    path('dashboard/doctors', views.doctors, name='doctors'),
    path('dashboard/doctors/add', views.add_doctor, name='add_doctor'),
    path('dashboard/doctors/get/<int:pk>', views.get_doctor, name='get_doctor'),
    path('dashboard/doctors/del/<int:pk>', views.del_doctor, name='del_doctor'),
    path('dashboard/doctors/edit/<int:pk>', views.edit_doctor, name='edit_doctor'),

    # Patients
    path('dashboard/patients', views.patients, name='patients'),
    path('dashboard/patients/add', views.add_patient, name='add_patient'),
    path('dashboard/patients/get/<int:pk>', views.get_patient, name='get_patient'),
    path('dashboard/patients/del/<int:pk>', views.del_patient, name='del_patient'),
    path('dashboard/patients/edit/<int:pk>', views.edit_patient, name='edit_patient'),

    # History
    path('dashboard/history', views.history, name='history'),
]

# handler404 = 'app.views.notfound'
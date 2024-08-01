from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('profiles/', include('user_profile.urls')),
    path('facilities/', include('facility_rental.urls')),
    path('tools/', include('tool_marketplace.urls')),
    path('payments/', include('payment.urls')),
]

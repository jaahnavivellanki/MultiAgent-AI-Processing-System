from django.urls import path
from .views import ProcessInputView
 
urlpatterns = [
    path('process/', ProcessInputView.as_view(), name='process-input'),
] 
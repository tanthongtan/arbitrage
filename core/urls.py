from django.urls import path, include
from django.views.generic.base import TemplateView

app_name = 'core'

# The URLs are now determined automatically by the router.
urlpatterns = [
    path('hello-webpack/', TemplateView.as_view(template_name='core/hello_webpack.html')),
]
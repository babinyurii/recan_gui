from django.urls import path
from app_recan_gui.views import recan_view
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", recan_view, name="recan_view"),
    path("example_datasets/", TemplateView.as_view(template_name='example_datasets.html'), name='datasets')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

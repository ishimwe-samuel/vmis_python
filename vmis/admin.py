from django.contrib import admin
from .models import VaccineStock, Vaccine
admin.autodiscover()
admin.site.enable_nav_sidebar = False
admin.site.site_header = "VMIS DASHBOARD"
admin.site.site_title = "vmis"
admin.site.index_title="VMIS APP"

admin.site.register(Vaccine)
admin.site.register(VaccineStock)

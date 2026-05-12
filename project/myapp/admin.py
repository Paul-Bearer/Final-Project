from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(FH_Location)
admin.site.register(Deceased_Info)
admin.site.register(Events)
admin.site.register(Finances)


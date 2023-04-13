from django.contrib import admin
from servicefinder.models import Userdetail,Contact,Partner,Booking,PartnerProfile,PartnerService,PartnerBookings
# Register your models here.

admin.site.register(Userdetail)
admin.site.register(Contact)
admin.site.register(Partner)
admin.site.register(Booking)
admin.site.register(PartnerProfile)
admin.site.register(PartnerService)
admin.site.register(PartnerBookings)
from django.contrib import admin
from .models import *

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", )

admin.site.register(Role)
admin.site.register(Person)
admin.site.register(Area)
admin.site.register(PersonImages)
admin.site.register(PersonFiles)
admin.site.register(Agent)
admin.site.register(Company)
admin.site.register(Administrator)
admin.site.register(Product)
admin.site.register(Price)
admin.site.register(Smeta)
admin.site.register(Contract)
admin.site.register(OnlineTransaction)
admin.site.register(Order)
admin.site.register(Specialization)
admin.site.register(University)
admin.site.register(Education)
admin.site.register(Comment)
admin.site.register(CommentImages)

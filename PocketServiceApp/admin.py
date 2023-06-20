from django.contrib import admin
from .models import *

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", )

admin.site.register(Role)
admin.site.register(Area)
admin.site.register(ImageObject)
admin.site.register(FileObject)
admin.site.register(Agent)
admin.site.register(Administrator)
admin.site.register(Product)
admin.site.register(Smeta)
admin.site.register(Contract)
admin.site.register(OnlineTransaction)

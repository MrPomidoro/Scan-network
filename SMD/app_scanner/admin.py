from django.contrib import admin
from .models import Local_Scanner, netmask, groupUp


@admin.register(Local_Scanner)
class Local_ScannerAdmin(admin.ModelAdmin):
    class Meta:
        model = Local_Scanner
        fields = '__all__'


@admin.register(netmask)
class netmaskAdmin(admin.ModelAdmin):
    class Meta:
        model = netmask
        fields = '__all__'


@admin.register(groupUp)
class netmaskAdmin(admin.ModelAdmin):
    class Meta:
        model = groupUp
        fields = '__all__'
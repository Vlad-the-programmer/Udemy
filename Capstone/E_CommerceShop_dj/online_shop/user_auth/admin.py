from django.contrib import admin
from django.contrib import admin
from .models import Customer, Profile

class CustomerAdmin(admin.ModelAdmin):
    fields = ('profile','first_name', 'last_name', 'username', 'phone', 
              'email', 'password', 'date_created')
    list_display = ('profile','first_name', 'last_name', 'username', 'phone', 
                    'email', 'password', 'date_created')
    
    fieldsets = (
      (None, {'fields': ('email', 'password', )}),
    )
    add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('email', 'password1', 'password2'),
      }),
    )

admin.site.register(Customer)
admin.site.register(Profile)
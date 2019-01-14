from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Singer)
admin.site.register(Company)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(PlayList)
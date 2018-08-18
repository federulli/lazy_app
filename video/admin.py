from django.contrib import admin

# Register your models here.
from .models import Torrent, Video, Season, Chapter

admin.site.register(Torrent)
admin.site.register(Video)
admin.site.register(Season)
admin.site.register(Chapter)

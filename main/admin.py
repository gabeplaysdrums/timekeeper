from django.contrib import admin
from main.models import *


class TimekeeperAdmin(admin.ModelAdmin):
  list_display = ('tempo', 'timesig_display', 'duration', 'feel', 'measures_per_phrase', 'request_count')
  list_display_links = ('request_count',)

  def timesig_display(self, obj):
    return '%d/%d' % (obj.timesig_numer, obj.timesig_denom)
  timesig_display.short_description = 'Time Signature'

admin.site.register(Timekeeper, TimekeeperAdmin)

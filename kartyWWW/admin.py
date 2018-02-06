from django.contrib import admin
from django.http import HttpResponse
from .models import *

def export_results_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"name"),
        smart_str(u"taskNumber"),
        smart_str(u"result"),
        smart_str(u"solutionTime"),
        smart_str(u"times"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.name),
            smart_str(obj.taskNumber),
            smart_str(obj.result),
            smart_str(obj.solutionTime),
            smart_str(obj.times),
        ])
    return response

def export_players_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"name"),
        smart_str(u"sex"),
        smart_str(u"age"),
        smart_str(u"active"),
        smart_str(u"gilSessionTimes"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.name),
            smart_str(obj.sex),
            smart_str(obj.age),
            smart_str(obj.active),
            smart_str(obj.gilSessionTimes),
        ])
    return response

export_results_csv.short_description = u"Export CSV"
export_players_csv.short_description = u"Export CSV"

class ResultAdmin(admin.ModelAdmin):
    actions = [export_results_csv]

class PlayerAdmin(admin.ModelAdmin):
    actions = [export_players_csv]

admin.site.register(AdminData)
admin.site.register(Player, PlayerAdmin)
admin.site.register(CardResult, ResultAdmin)
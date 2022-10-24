from import_export import resources
from data.models import Log

#https://simpleisbetterthancomplex.com/packages/2016/08/11/django-import-export.html

class Log(resources.ModelResource):
    class Meta:
        model = Log
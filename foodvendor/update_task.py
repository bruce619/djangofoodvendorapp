from background_task import background
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
import json


class ExtendedEncoder(DjangoJSONEncoder):

    def default(self, o):

        if isinstance(o, Model):
            return model_to_dict(o)

        return super().default(o)


@background(schedule=60)
def update_date(obj, datetimecreated, new_date):
    obj.objects.get(datetimecreated=datetimecreated)
    obj.objects.update(datetimecreated=new_date)
    obj.save()
    json.dumps(obj, cls=ExtendedEncoder)

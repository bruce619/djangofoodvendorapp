from background_task import background


@background(schedule=60)
def update_date(obj, datetimecreated, new_date):
    obj.objects.get(datetimecreated=datetimecreated)
    obj.objects.update(datetimecreated=new_date)
    obj.save()

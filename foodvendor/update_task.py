from background_task import background


@background(schedule=60)
def update_date(menu_date, new_date=None):
    days_after = (menu_date + new_date).isoformat()
    return days_after


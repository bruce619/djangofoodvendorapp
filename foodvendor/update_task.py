from background_task import background


@background(schedule=60)
def update_date(menu_date, new_date=None):
    menu_date += new_date
    return menu_date


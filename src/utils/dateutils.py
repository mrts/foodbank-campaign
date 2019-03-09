import datetime

# Python 3.6 doesn't have fromisoformat, use `pip install backports-datetime-fromisoformat`
if not hasattr(datetime.date, 'fromisoformat'):
    from backports.datetime_fromisoformat import MonkeyPatch
    MonkeyPatch.patch_fromisoformat()

def get_first_second_day_from_arg(arg):
    first_day = datetime.date.fromisoformat(arg)
    second_day = first_day + datetime.timedelta(days=1)
    return first_day, second_day

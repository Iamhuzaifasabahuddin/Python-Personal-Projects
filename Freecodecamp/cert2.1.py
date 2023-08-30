import datetime as dt


def add_time(start, duration, day=None):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    start_time, period = start.split()
    start_hour, start_minute = map(int, start_time.split(':'))

    duration_hour, duration_minute = map(int, duration.split(':'))

    # if period == 'PM':
    #     start_hour += 12
    # start_time = dt.datetime(1, 1, 1, start_hour, start_minute)
    # duration_time = dt.timedelta(hours=duration_hour, minutes=duration_minute)

    new_minute = (start_minute + duration_minute) % 60
    hour_change = (start_minute + duration_minute) // 60

    if period == 'PM':
        start_hour += 12

    new_hour = (start_hour + duration_hour + hour_change) % 24

    # new_time = start_time + duration_time

    # new_hour = new_time.hour
    # new_minute = new_time.minute

    new_period = 'AM'
    if new_hour >= 12:
        new_period = 'PM'
    if new_hour == 0:
        new_hour = 12
    elif new_hour > 12:
        new_hour -= 12

    days_passed = (start_hour + duration_hour + hour_change) // 24
    # days_passed = (start_time+ duration_time).date() - start_time.date()
    # We subtract startime to get whether the day has been passed i.e 25 hours - 24 hours would result in 1 am
    if day:
        day = day.capitalize()
        day_index = days_of_week.index(day)
        new_day_index = (day_index + days_passed) % 7  # or days_passed.days when using datetime method
        new_day = days_of_week[new_day_index]
        new_time = f"{new_hour}:{new_minute:02d} {new_period}, {new_day}"
    else:
        new_time = f"{new_hour}:{new_minute:02d} {new_period}"

    if days_passed == 1:  # or days_passed.days when using datetime method
        new_time += " (next day)"
    elif days_passed > 1:  # or days_passed.days when using datetime method
        new_time += f" ({days_passed} days later)"

    return new_time


if __name__ == '__main__':
    print(add_time("11:06 PM", "2:02", "Monday"))  # Output: "01:08 AM (next day)"
    # print(add_time("3:00 PM", "3:10"))  # Output: "06:10 PM"
    # print(add_time("11:30 AM", "2:32", "Monday"))  # Output: "02:02 PM, Tuesday"

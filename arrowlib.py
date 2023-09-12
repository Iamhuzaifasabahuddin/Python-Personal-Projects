import arrow

selected_date = '2023-09-11'

date = arrow.get(selected_date)

end_of_month = date.ceil('month')

end_of_month_str = end_of_month.format('YYYY-MM-DD')

print(f"The end date of the month for {selected_date} is {end_of_month_str}")

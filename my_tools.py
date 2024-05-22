#!/usr/bin/python3
''' tools module '''
from datetime import datetime
import re
# Module of regular expression is used with search()


def calculate_age(birthday):
	"""function that detemine the age"""

	if not isinstance(birthday, (str, datetime)):
		return 'unable to find age'

	if isinstance(birthday, str):
		try:
			date_obj = datetime.strptime(birthday, '%Y-%m-%d')
		except ValueError:
			return 'unable to find age'

	if isinstance(birthday, datetime):
		date_obj = birthday

	current_date = datetime.today().date()
	current_year = current_date.year
	current_month = current_date.month
	current_day = current_date.day

	age = current_year - date_obj.year

	if current_month < date_obj.month or (current_month == date_obj.month and current_day < date_obj.day):
		age -= 1

	return age


def valid_password(password):
	""" function that checks validation of password """
	while True:
		if (len(password) <= 8):
			message = 'password must be at least 8 letters length'
			break
		elif not re.search("[a-z]", password):
			message = 'password should contain at least one letter [a-z]'
			break
		elif not re.search("[A-Z]", password):
			message = 'password should contain at least one letter [A-Z]'
			break
		elif not re.search("[0-9]", password):
			message = 'password should contain At least 1 digit between [0-9]'
			break
		else:
			message = True
			break

	return message


# print(valid_password('hbvbh'))
# print(valid_password('616266445415614'))
# print(valid_password('vcfevfevfedecef'))
# print(valid_password('vcfevaAfedegtcef'))
# print(valid_password('vcfevfe7fAedecef'))
# print(valid_password('aAbB7dcdcdcxdc'))


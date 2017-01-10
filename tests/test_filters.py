import os
import unittest
import datetime

#Configure your app to use the testing configuration
if not "CONFIG_PATH" in os.environ:
	os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

import blog
from blog.filters import *

class FilterTests(unittest.TestCase):
	def test_date_format(self):
		date = datetime.date(1999, 12, 31)
		formatted = dateformat(date, "%m/%y/%d")
		self.assertEqual(formatted, "12/99/31")

	def test_date_format_none(self):
		formatted = dateformat(None, "%m/%y/%d")
		self.assertEqual(formatted, None)


if __name__ == "__main__":
	unittest.main()
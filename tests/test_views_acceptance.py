import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

if not "CONFIG_PATH" in os.environ:
	os.environ["CONFIG_PATH"] = "blog.config.TravisConfig"

from blog import app
from blog.database import Base, engine, session, User

class TestViews(unittest.TestCase):
	def setUp(self):

		self.browser = Browser("phantomjs")
		Base.metadata.create_all(engine)

		self.user = User(name="Jim", email="jim@test.com",
						password=generate_password_hash("test"))
		session.add(self.user)
		session.commit()

		self.process = multiprocessing.Process(target=app.run,
												kwargs={"port": 8080})
		self.process.start()
		time.sleep(1)

	def test_login_correct(self):
		self.browser.visit("http://0.0.0.0:8080/login")
		self.browser.fill("email", "jim@test.com")
		self.browser.fill("password", "test")
		button = self.browser.find_by_css("button[type=submit]")
		button.click()
		self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")

	def test_create_entry(self):
		#login
		self.browser.visit("http://0.0.0.0:8080/login")
		self.browser.fill("email", "jim@test.com")
		self.browser.fill("password", "test")
		button = self.browser.find_by_css("button[type=submit]")
		button.click()
		#new entry
		self.browser.visit("http://0.0.0.0:8080/entry/add")
		self.browser.fill("title", "This is a test Title")
		self.browser.fill("content", "Lorem Ipsum Dolor nunc....")
		button = self.browser.find_by_css("button[type=submit]")
		button.click()
		self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")

	def test_login_incorrect(self):
		self.browser.visit("http://0.0.0.0:8080/login")
		self.browser.fill("email", "bob@example.com")
		self.browser.fill("password", "test")
		button = self.browser.find_by_css("button[type=submit]")
		button.click()
		self.assertEqual(self.browser.url, "http://0.0.0.0:8080/login")

	def test_pagination(self):
		#login
		self.browser.visit("http://0.0.0.0:8080/login")
		self.browser.fill("email", "jim@test.com")
		self.browser.fill("password", "test")
		button = self.browser.find_by_css("button[type=submit]")
		button.click()
		self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")
		#make a bunch of entries
		for entry in range(21):
			self.browser.visit("http://0.0.0.0:8080/entry/add")
			self.browser.fill("title", "This is a test Title{}".format(entry))
			self.browser.fill("content", "Lorem Ipsum Dolor nunc....")
			button = self.browser.find_by_css("button[type=submit]")
			button.click()
			self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")
		#test pagination
		self.browser.visit("http://0.0.0.0:8080/")
		element = self.browser.find_by_xpath('//select').first
		element.select('10')
		button = self.browser.find_by_css("button[type=submit]")
		button.click()
		self.assertEqual(self.browser.url, "http://0.0.0.0:8080/?entries_per=10")

	def tearDown(self):
		self.process.terminate()
		session.close()
		engine.dispose()
		Base.metadata.drop_all(engine)
		self.browser.quit()

if __name__ == "__main__":
	unittest.main()

import os
import unittest
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash

os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User, Entry

class TestViews(unittest.TestCase):
	def setUp(self):
		"""Test Setup"""
		self.client = app.test_client()

		#set up tables in db
		Base.metadata.create_all(engine)

		#create a user
		self.user = User(name="Alice", email="alice@test.com",
						password=generate_password_hash("test"))
		session.add(self.user)
		session.commit()

	def tearDown(self):
		""" Test teardown"""
		session.close()
		#remove tables and data from DB
		Base.metadata.drop_all(engine)

	def simulate_login(self):
		with self.client.session_transaction() as http_session:
			http_session["user_id"] = str(self.user.id)
			http_session["_fresh"] = True

	def test_add_edit_entry(self):
		self.simulate_login()

		response = self.client.post("/entry/add", data={
			"title": "Test Entry",
			"content": "Test content"
			})

		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/")
		entries = session.query(Entry).all()
		self.assertEqual(len(entries), 1)

		entry = entries[0]
		self.assertEqual(entry.title, "Test Entry")
		self.assertEqual(entry.content, "Test content")
		self.assertEqual(entry.author, self.user)

		response = self.client.post("/entry/1/edit", data={
			"title": "Edited Test Entry",
			"content": "Edited Test Content"
			})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/")
		entries = session.query(Entry).all()
		self.assertEqual(len(entries), 1)

		entry = entries[0]
		self.assertEqual(entry.title, "Edited Test Entry")
		self.assertEqual(entry.content, "Edited Test Content")

	def test_delete_entry(self):
		self.simulate_login()

		response = self.client.post("/entry/add", data={
			"title": "Test Entry",
			"content": "Test content"
			})

		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/")
		entries = session.query(Entry).all()
		self.assertEqual(len(entries), 1)

		entry = entries[0]
		self.assertEqual(entry.title, "Test Entry")
		self.assertEqual(entry.content, "Test content")
		self.assertEqual(entry.author, self.user)

		response = self.client.post("/entry/1/delete")

		entries = session.query(Entry).all()
		self.assertEqual(len(entries), 0)

	def test_create_user(self):
		self.simulate_login()

		response = self.client.post("/newuser", data={
			"name": "Nick Test",
			"email": "testemail@test.com",
			"password": "testpassword"
			})

		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/")
		users = session.query(User).all()
		self.assertEqual(len(users), 2)

		user = users[1]
		self.assertEqual(user.name, "Nick Test")
		self.assertEqual(user.email, "testemail@test.com")
		self.assertNotEqual(user.password, "testpassword")


if __name__ == "__main__":
	unittest.main()



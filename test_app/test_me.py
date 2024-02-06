from unittest import TestCase

from app import app
from models import User, db, default_img


class UserDatabaseTests(TestCase):

    def setUp(self):
        with app.app_context():
            db.create_all()

            User.query.delete()

            new_user = User(
                first_name="Henrik", last_name="Sedin", image_url=default_img
            )
            db.session.add(new_user)
            db.session.commit()

            self.user_id = new_user.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()

    def test_users_list(self):
        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Henrik", html)

    def test_user_details(self):
        with app.test_client() as client:
            response = client.get(f"/user_details/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h1>Henrik Sedin</h1>", html)

    def test_add_user(self):
        with app.test_client() as client:
            user_2 = {
                "first_name": "Quinn",
                "last_name": "Hughes",
                "image_url": default_img,
            }
            response = client.post("/create_user", data=user_2, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Quinn Hughes</a>", html)

    def test_delete_user(self):
        with app.test_client() as client:
            response = client.post(
                f"/delete_user", data=self.user_id, follow_redirects=True
            )
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn("Henrik", html)

    def test_edit_user(self):
        with app.test_client() as client:
            update_name = {
                "first_name": "Daniel",
                "last_name": "Sedin",
                "image_url": "",
            }
            response = client.post(
                f"/edit_user/{self.user_id}", data=update_name, follow_redirects=True
            )
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h1>Daniel Sedin</h1>", html)

from unittest import TestCase

from app import app, db
from models import Posts, User, default_img


class PostsDatabaseTests(TestCase):
    def setUp(self):
        with app.app_context():
            app.config["TESTING"] = True

            user = User(first_name="Daniel", last_name="Sedin", image_url=default_img)
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

            post = Posts(
                title="Test Post", content="Nothing here.", user_id=self.user_id
            )

            db.session.add(post)
            db.session.commit()
            self.post_id = post.id

    def tearDown(self):
        with app.app_context():
            Posts.query.delete()
            User.query.delete()

    def test_create_post(self):
        with app.test_client() as client:
            new_post = {"post-title": "Test Post", "post-content": "lorem ipsum"}
            response = client.post(
                f"/users/{self.user_id}/posts/new", data=new_post, follow_redirects=True
            )

            retrieved_post = Posts.query.filter_by(title="Test Post").first()

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(retrieved_post)
            self.assertEqual(retrieved_post.user_id, self.user_id)
            self.assertEqual(db.session.query(Posts).count(), 2)

    def test_edit_post(self):
        with app.test_client() as client:
            edit_data = {
                "post-title": "Edited Post",
                "post-content": "lorem lorem lorem",
            }
            response = client.post(
                f"/posts/{self.post_id}/edit", data=edit_data, follow_redirects=True
            )

            edited_post = Posts.query.get(self.post_id)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(edited_post.title, "Edited Post")
            self.assertEqual(edited_post.content, "lorem lorem lorem")

    def test_delete_post(self):
        with app.test_client() as client:
            response = client.post(
                f"/posts/{self.post_id}/delete", follow_redirects=True
            )

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn("Test Post", html)
            self.assertEqual(db.session.query(Posts).count(), 0)

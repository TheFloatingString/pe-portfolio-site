# tests.py
import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(":memory:")


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(
            name="John Doe", email="john@example.com", content="Hello World, I'm John!"
        )
        assert first_post.id == 1
        second_post = TimelinePost.create(
            name="Jane Doe", email="jane@example.com", content="Hello World, I'm Jane!"
        )
        assert second_post.id == 2
        
        # TODO: Get all posts and assert that we have 2 posts in the database
        # Hint: TimelinePost.select().count()
        posts_count = TimelinePost.select().count()
        assert posts_count == 2
        
        # Get all posts and check their content
        all_posts = list(TimelinePost.select())
        assert len(all_posts) == 2
        assert all_posts[0].name == "John Doe"
        assert all_posts[1].name == "Jane Doe"
        
        # Test updating a post
        first_post.content = "Updated content"
        first_post.save()
        updated_post = TimelinePost.get(TimelinePost.id == 1)
        assert updated_post.content == "Updated content"
        
        # Test deleting a post
        second_post.delete_instance()
        remaining_posts = TimelinePost.select().count()
        assert remaining_posts == 1

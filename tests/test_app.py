import unittest
import os

os.environ["TESTING"] = "true"

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        # TODO: Add more tests for homepage
        # Test that the page contains expected elements
        assert "MLH Fellow" in html
        assert "<body" in html
        assert "</body>" in html
        assert "<html" in html
        assert "</html>" in html

    def test_timeline(self):
        # Test the timeline page
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Timeline" in html
        
        # Test the timeline API endpoint
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        # TODO: add more tests to timeline get/post, and timeline page
        
        # Test posting to the timeline
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Test User",
                "email": "test@example.com",
                "content": "Test content"
            }
        )
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json["name"] == "Test User"
        assert json["email"] == "test@example.com"
        assert json["content"] == "Test content"
        
        # Test that the post was added to the timeline
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json = response.get_json()
        assert len(json["timeline_posts"]) > 0
        assert json["timeline_posts"][0]["name"] == "Test User"
        assert json["timeline_posts"][0]["email"] == "test@example.com"
        assert json["timeline_posts"][0]["content"] == "Test content"

    def test_hobbies(self):
        # Test the hobbies page
        response = self.client.get("/hobbies")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "biking" in html
        assert "guitar" in html
        assert "running" in html

    def test_malformed_timeline_post(self):
        # missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello World, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Name" in html

        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Content" in html

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello World, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Email" in html

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import ShortURL


class ShortURLAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url_data = {"url": "https://www.example.com/some/long/url"}
        self.short_url = ShortURL.objects.create(
            url="https://www.example.com/initial",
            short_code="init12",
        )

    def test_create_short_url(self):
        response = self.client.post("/shorten", self.url_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_code", response.data)
        self.assertEqual(response.data["url"], self.url_data["url"])
        self.assertEqual(response.data["access_count"], 0)

    def test_create_short_url_invalid(self):
        response = self.client.post("/shorten", {"url": "not-a-url"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_short_url_empty(self):
        response = self.client.post("/shorten", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_original_url(self):
        response = self.client.get(f"/shorten/{self.short_url.short_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["url"], self.short_url.url)

    def test_retrieve_original_url_not_found(self):
        response = self.client.get("/shorten/nonexist")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_short_url(self):
        update_data = {"url": "https://www.example.com/updated"}
        response = self.client.put(
            f"/shorten/{self.short_url.short_code}", update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["url"], update_data["url"])

    def test_update_short_url_not_found(self):
        response = self.client.put(
            "/shorten/nonexist", {"url": "https://example.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_short_url_invalid(self):
        response = self.client.put(
            f"/shorten/{self.short_url.short_code}",
            {"url": "not-a-url"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_short_url(self):
        response = self.client.delete(f"/shorten/{self.short_url.short_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ShortURL.objects.filter(short_code=self.short_url.short_code).exists())

    def test_delete_short_url_not_found(self):
        response = self.client.delete("/shorten/nonexist")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_stats(self):
        response = self.client.get(f"/shorten/{self.short_url.short_code}/stats")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_count", response.data)
        self.assertEqual(response.data["access_count"], 0)

    def test_get_stats_not_found(self):
        response = self.client.get("/shorten/nonexist/stats")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_redirect_increments_access_count(self):
        response = self.client.get(f"/{self.short_url.short_code}")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.short_url.refresh_from_db()
        self.assertEqual(self.short_url.access_count, 1)

    def test_redirect_not_found(self):
        response = self.client.get("/nonexist")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

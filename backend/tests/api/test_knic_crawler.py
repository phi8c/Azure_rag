import unittest
from unittest.mock import patch

import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.website_crawl_router import router
from app.services.knic_crawler import extract_page, fetch_html, normalize_url, crawl_knic


class KnicCrawlerTest(unittest.IsolatedAsyncioTestCase):
    def test_scope_and_clean_text(self):
        for url in ("https://other.test/vi/", "http://knic.com.vn/vi/", "/en/", "/vi/?s=x"):
            self.assertIsNone(normalize_url(url))
        title, text, links = extract_page(
            '<title>KNIC</title><nav>Menu</nav><main><h1>Công ty</h1>'
            '<p>Thông tin đối tác</p><script>hidden</script></main>'
            '<a href="/vi/about/#x">About</a><a href="/en/">EN</a>',
            "https://knic.com.vn/vi/",
        )
        self.assertEqual(title, "KNIC")
        self.assertIn("Thông tin đối tác", text)
        self.assertNotIn("hidden", text)
        self.assertNotIn("Menu", text)
        self.assertEqual(links, ["https://knic.com.vn/vi/about/"])

    async def test_redirect_outside_scope_is_never_requested(self):
        requested = []

        def handle(request):
            requested.append(str(request.url))
            return httpx.Response(302, headers={"location": "https://other.test/vi/"})

        async with httpx.AsyncClient(transport=httpx.MockTransport(handle)) as client:
            with self.assertRaises(ValueError):
                await fetch_html(client, "https://knic.com.vn/vi/")
        self.assertEqual(requested, ["https://knic.com.vn/vi/"])

    async def test_partial_failure_is_recorded_and_duplicate_links_are_not_fetched(self):
        calls = []

        async def fetch(client, url):
            calls.append(url)
            if url.endswith("bad/"):
                raise ValueError("Unavailable")
            return url, '<main>Công ty KNIC</main><a href="/vi/bad/">Bad</a><a href="/vi/bad/#x">Bad</a>'

        with patch("app.services.knic_crawler.fetch_html", side_effect=fetch):
            filename, content = await crawl_knic(3, 1)
        self.assertTrue(filename.endswith(".txt"))
        self.assertIn("Công ty KNIC", content.decode("utf-8"))
        self.assertIn("Unavailable", content.decode("utf-8"))
        self.assertEqual(len(calls), 2)

    def test_download_and_validation(self):
        app = FastAPI()
        app.include_router(router)
        with TestClient(app) as client:
            with patch("app.api.v1.website_crawl_router.crawl_knic", return_value=("knic.txt", b"KNIC")):
                response = client.post("/documents/crawl/knic", json={"max_pages": 1})
            self.assertEqual(response.status_code, 200)
            self.assertIn('filename="knic.txt"', response.headers["content-disposition"])
            self.assertEqual(response.content, b"KNIC")
            self.assertEqual(client.post("/documents/crawl/knic", json={"max_pages": 61}).status_code, 422)

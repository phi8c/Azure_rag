"""Bounded KNIC HTML crawl shared by the API and command-line script."""

import asyncio
from collections import deque
from datetime import datetime, timezone
from urllib.parse import urljoin, urlsplit, urlunsplit

import httpx
from bs4 import BeautifulSoup


START_URL = "https://knic.com.vn/vi/"
MAX_PAGE_BYTES = 3_000_000


def normalize_url(url: str, base: str = START_URL) -> str | None:
    parsed = urlsplit(urljoin(base, url))
    if (
        parsed.scheme != "https"
        or parsed.netloc.lower() != "knic.com.vn"
        or not parsed.path.startswith("/vi/")
        or parsed.query
    ):
        return None
    if parsed.path.lower().endswith(
        (".pdf", ".jpg", ".jpeg", ".png", ".svg", ".zip", ".mp4", ".webp")
    ):
        return None
    return urlunsplit(("https", "knic.com.vn", parsed.path, "", ""))


async def fetch_html(client: httpx.AsyncClient, url: str) -> tuple[str, str]:
    # Validate every redirect before issuing another request.
    for _ in range(6):
        async with client.stream("GET", url) as response:
            if response.is_redirect:
                target = normalize_url(response.headers.get("location", ""), url)
                if not target:
                    raise ValueError("Redirect outside the allowed KNIC Vietnamese pages")
                url = target
                continue
            response.raise_for_status()
            if "text/html" not in response.headers.get("content-type", "").lower():
                raise ValueError("Not an HTML page")
            data = bytearray()
            async for chunk in response.aiter_bytes():
                data.extend(chunk)
                if len(data) > MAX_PAGE_BYTES:
                    raise ValueError("Page exceeds 3 MB limit")
            return url, data.decode(response.encoding or "utf-8", errors="replace")
    raise ValueError("Too many redirects")


def extract_page(html: str, url: str) -> tuple[str, str, list[str]]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else url
    links = list(dict.fromkeys(
        target for anchor in soup.select("a[href]")
        if (target := normalize_url(anchor.get("href", ""), url))
    ))
    for element in soup.select("script, style, noscript, nav, header, footer, form, svg"):
        element.decompose()
    content = soup.find("main") or soup.find("article") or soup.body or soup
    lines = [" ".join(line.split()) for line in content.get_text("\n", strip=True).splitlines()]
    return title, "\n".join(line for line in lines if line), links


async def _crawl_knic(max_pages: int, max_depth: int) -> tuple[str, bytes]:
    if not 1 <= max_pages <= 60 or not 0 <= max_depth <= 4:
        raise ValueError("max_pages must be 1..60; max_depth must be 0..4")
    started = datetime.now(timezone.utc)
    queue = deque([(START_URL, 0)])
    scheduled = {START_URL}
    visited = set()
    pages = []
    failures = []
    attempted = 0
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(15.0), follow_redirects=False,
        headers={"User-Agent": "AzureAuto-KNICCrawler/1.0", "Accept": "text/html"},
    ) as client:
        while queue and attempted < max_pages:
            url, depth = queue.popleft()
            if url in visited:
                continue
            attempted += 1
            try:
                final_url, html = await fetch_html(client, url)
                if final_url in visited:
                    continue
                visited.update((url, final_url))
                title, text, links = extract_page(html, final_url)
                if not text:
                    raise ValueError("No readable text found")
                pages.append((title, final_url, text))
                if depth < max_depth:
                    for link in links:
                        if link not in scheduled and len(scheduled) < 1000:
                            scheduled.add(link)
                            queue.append((link, depth + 1))
            except (httpx.HTTPError, ValueError) as exc:
                failures.append((url, str(exc)))
            await asyncio.sleep(0.25)
    if not pages:
        raise ValueError("Unable to extract any KNIC pages")
    lines = [
        "KNIC - THÔNG TIN THU THẬP TỪ WEBSITE", f"Nguồn: {START_URL}",
        f"Thời điểm bắt đầu (UTC): {started.isoformat()}",
        f"Thời điểm hoàn tất (UTC): {datetime.now(timezone.utc).isoformat()}",
        f"Số trang thành công: {len(pages)}; số trang lỗi: {len(failures)}",
        f"Giới hạn: {max_pages} lượt tải, độ sâu {max_depth}.",
        f"Còn URL chờ xử lý: {len(queue)}",
        "Nội dung trích xuất từ HTML, không phải bản tóm tắt đã xác minh.",
        "Không bao gồm PDF, hình ảnh, video hoặc nội dung cần JavaScript.", "",
    ]
    for index, (title, url, text) in enumerate(pages, 1):
        lines.extend(["=" * 72, f"{index}. {title}", f"URL nguồn: {url}", "", text, ""])
    if failures:
        lines.extend(["TRANG KHÔNG THU THẬP ĐƯỢC", *[f"{url}: {error}" for url, error in failures]])
    filename = f"knic_company_info_{started.strftime('%Y%m%dT%H%M%S%fZ')}.txt"
    return filename, "\n".join(lines).encode("utf-8")


async def crawl_knic(max_pages: int = 30, max_depth: int = 2) -> tuple[str, bytes]:
    return await asyncio.wait_for(_crawl_knic(max_pages, max_depth), timeout=180)

"""S1: the top bar has four doors, and nothing was hidden: every page is still reachable by clicking from the landing page."""
import re

PAGES = {"/", "/me", "/monitor", "/attention", "/mission", "/dashboard", "/brief", "/replay", "/evidence", "/about"}


def test_top_bar_has_four_links_and_one_action(client):
    html = client.get("/").get_data(as_text=True)
    nav = re.search(r'<nav class="nav-links".*?</nav>', html, re.S).group(0)
    assert re.findall(r">([^<]+)</a>", nav) == ["My check-in", "Reviewer", "Evidence", "Privacy &amp; limits"]
    assert "Start check-in" in html


def test_every_page_is_reachable_by_links_from_the_landing_page(client):
    seen, queue = set(), ["/"]
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        html = client.get(path).get_data(as_text=True)
        for href in re.findall(r'href="(/[^"#?]*)', html):
            if href in PAGES and href not in seen:
                queue.append(href)
    assert PAGES <= seen, f"unreachable by clicking: {sorted(PAGES - seen)}"

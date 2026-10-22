"""Regression test for: Subtotal not updated after removing an item

Written by Repro from the screen recording shoplite-remove.mp4. It failed before the fix and passes after it.

Run it against a running app:
    pip install pytest-playwright && playwright install chromium
    pytest e2e --base-url http://localhost:3000
"""

from playwright.sync_api import expect

def test_repro(page, base_url):
    # Step 1 (t=0.62s): hover Coupon code input field
    page.goto(base_url)
    page.get_by_test_id("coupon-input").hover()
    # Step 2 (t=1.81s): click Add to cart (Logo Cap card)
    page.get_by_test_id("add-cap").click()
    # Step 3 (t=3.44s): click Add to cart (Sticker Pack card)
    page.get_by_test_id("add-stickers").click()
    # Step 4 (t=5.0s): click Add to cart (Dev Mug card)
    page.get_by_test_id("add-mug").click()
    # Step 5 (t=7.19s): click Remove (Logo Cap row)
    page.get_by_test_id("remove-cap").click()
    # Verify cart totals after removal
    expect(page.get_by_test_id("subtotal")).to_have_text("$17.49")
    expect(page.get_by_test_id("total")).to_have_text("$22.48")

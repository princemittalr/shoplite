"""Regression test for: Coupon code applies discount multiple times when applied repeatedly

Written by Repro from the screen recording shoplite-coupon.mp4. It failed before the fix and passes after it.

Run it against a running app:
    pip install pytest-playwright && playwright install chromium
    pytest e2e --base-url http://localhost:3000
"""

from playwright.sync_api import expect

def test_repro(page, base_url):
    page.goto(base_url)
    # Step 1 (t=2.06s): click Add to cart (Classic Tee card)
    page.get_by_test_id("add-tee").click()
    # Step 2 (t=3.69s): click Add to cart (Dev Mug card)
    page.get_by_test_id("add-mug").click()
    # Step 3 (t=6.19s): type coupon code SAVE10
    page.get_by_test_id("coupon-input").fill("SAVE10")
    # Step 4 (t=7.44s): click Apply button
    page.get_by_test_id("apply-coupon").click()
    # Capture discount and total after first apply
    discount_after_first = page.get_by_test_id("discount").inner_text()
    total_after_first = page.get_by_test_id("total").inner_text()
    # Step 5 (t=10.62s): type coupon code SAVE10 again
    page.get_by_test_id("coupon-input").fill("SAVE10")
    # Step 6 (t=11.94s): click Apply button again
    page.get_by_test_id("apply-coupon").click()
    # Assert discount and total unchanged (prevents stacking)
    expect(page.get_by_test_id("discount")).to_have_text(discount_after_first)
    expect(page.get_by_test_id("total")).to_have_text(total_after_first)

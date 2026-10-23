// Test for duplicate coupon application not stacking discount
import { test } from "node:test";
import assert from "node:assert/strict";

import {
  addItem, applyCoupon, createCart, totals,
} from "../public/cart.js";

test("applying the same coupon twice does not stack discount", () => {
  const cart = addItem(createCart(), "tee"); // $19.99
  addItem(cart, "mug"); // $12.50 -> subtotal $32.49

  // First apply
  const result1 = applyCoupon(cart, "SAVE10");
  assert.equal(result1.ok, true);
  // Discount should be 10% of 3249 cents = 324.9 -> rounded? In cart.js they use Math.round((subtotal * value)/100)
  // 3249 * 10 / 100 = 324.9 -> Math.round => 325 cents ($3.25)
  assert.equal(totals(cart).discount, 325);

  // Second apply of same coupon
  const result2 = applyCoupon(cart, "SAVE10");
  assert.equal(result2.ok, true);
  // Message indicates already applied
  assert.equal(result2.message, "Coupon SAVE10 is already applied.");
  // Discount should remain the same
  assert.equal(totals(cart).discount, 325);
});

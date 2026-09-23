import { expect, test } from "bun:test";

import { decideApproval } from "./pure-policy";

test("an open account at its limit is approved", () => {
  expect(decideApproval({ accountOpen: true, requested: 10, limit: 10 })).toEqual({ _tag: "Approve" });
});

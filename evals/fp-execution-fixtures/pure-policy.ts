export type ApprovalDecision =
  | { readonly _tag: "Approve" }
  | { readonly _tag: "Reject"; readonly reason: "limit-exceeded" | "account-closed" };

export const decideApproval = (input: {
  readonly accountOpen: boolean;
  readonly requested: number;
  readonly limit: number;
}): ApprovalDecision => {
  if (!input.accountOpen) return { _tag: "Reject", reason: "account-closed" };
  if (input.requested > input.limit) return { _tag: "Reject", reason: "limit-exceeded" };
  return { _tag: "Approve" };
};

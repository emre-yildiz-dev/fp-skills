export type LinkDecision =
  | { readonly _tag: "SignIn"; readonly userId: string }
  | { readonly _tag: "CreateUser"; readonly email: string }
  | { readonly _tag: "RejectNotLinked"; readonly email: string };

export const decideLinking = (input: {
  readonly linkedUserId: string | null;
  readonly existingEmailOwnerId: string | null;
  readonly email: string;
}): LinkDecision => {
  if (input.linkedUserId !== null) return { _tag: "SignIn", userId: input.linkedUserId };
  if (input.existingEmailOwnerId !== null) return { _tag: "RejectNotLinked", email: input.email };
  return { _tag: "CreateUser", email: input.email };
};

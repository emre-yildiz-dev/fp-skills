import { createServer } from "node:http";

import { Effect } from "effect";

import { getById } from "./wrong-500-handler";

const expectedStatus = Number(Bun.env.EXPECT_STATUS ?? "404");
const server = createServer(async (request, response) => {
  if (request.url !== "/items/missing") {
    response.statusCode = 404;
    response.end();
    return;
  }

  try {
    response.statusCode = await Effect.runPromise(
      getById(Effect.succeed([]), "missing").pipe(
        Effect.match({
          onFailure: (error) => error._tag === "NotFound" ? 404 : 500,
          onSuccess: () => 200,
        }),
      ),
    );
  } catch {
    // The harness deliberately exposes only the status, never a raw Cause or failure payload.
    response.statusCode = 500;
  }
  response.end();
});

await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
try {
  const address = server.address();
  if (!address || typeof address === "string") throw new Error("server did not bind a TCP address");

  const response = await fetch(`http://127.0.0.1:${address.port}/items/missing`);
  if (response.status !== expectedStatus) {
    throw new Error(`expected HTTP ${expectedStatus}, received HTTP ${response.status}`);
  }
} finally {
  await new Promise<void>((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

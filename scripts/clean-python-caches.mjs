import { readdirSync, rmSync } from "node:fs";
import { join } from "node:path";

function removePythonCaches(directory) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (!entry.isDirectory()) continue;
    if (entry.name === "__pycache__") {
      rmSync(path, { recursive: true, force: true });
    } else {
      removePythonCaches(path);
    }
  }
}

removePythonCaches(".agents/skills/fp");

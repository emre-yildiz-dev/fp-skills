# Effect 4.0.0-rc.111 Fixture Provenance

These fixtures were copied on 2026-09-23 from the installed dependency and resolved lock in the Effect backend template checkout at `/Users/emre/code/test/effect-backend` (template commit `0e4be21be6a6f6454b8d5423dea6ded426c3bec1`). They are evidence for RC.111 only; they must not be generalized to another Effect release.

| Fixture | Exact source | Extraction | Source SHA-256 | Fixture SHA-256 |
|---|---|---|---|---|
| `effect-resolved-lock.txt` | `bun.lock` | line 1715, the complete `effect` package resolution entry | `d5a0073e0becb536e7d7a327e75f762403f2b95abea51fd826129acee73ec37c` | `42b33d0c0f0a6659f32fe1ae0e09bd65856851cb3b4e416cd2c44cff3889205a` |
| `effect-rc111-package.json` | `node_modules/.bun/effect@4.0.0-rc.111/node_modules/effect/package.json` | complete file | `5bc5f8e5f799ae66691c35a0b64d262e681b37a26a67a665abf0cd95e0da5847` | `5bc5f8e5f799ae66691c35a0b64d262e681b37a26a67a665abf0cd95e0da5847` |
| `effect-rc111-context-service.d.ts` | `node_modules/.bun/effect@4.0.0-rc.111/node_modules/effect/dist/Context.d.ts` | lines 188-350, the complete `Service` declaration | `0426deb9b04e9366993f3d84d937fb39086a0cbd97bb3680e9ce67ca6c3255ae` | `6415bccd414ee5a85bdb0aa1059c767afa40eb6c19da4ed0f69ce34d1b709851` |
| `effect-rc111-layer-effect.d.ts` | `node_modules/.bun/effect@4.0.0-rc.111/node_modules/effect/dist/Layer.d.ts` | lines 1131-1210, the complete `effect` declaration | `1ee58098059d4a2286697c3fae0c185bf62e77ce8677884db4079752926642a7` | `94c13302c0ee35eac5dec007e17f1215c0228d30ff403f66b7c22d9b3791b1fe` |
| `effect-rc111-layer-provide.d.ts` | same installed `dist/Layer.d.ts` | lines 1704-2029, the complete `provide` declaration | `1ee58098059d4a2286697c3fae0c185bf62e77ce8677884db4079752926642a7` | `e2cbc1cb0fdba6758fa0c0b51b80942e8502f654db4a217bef8f85657d687985` |

The lock entry resolves `effect@4.0.0-rc.111` with integrity `sha512-ASd5L58EIR0CUNueZNKKjSsyOCd+2alxOAIaTcHaqkJkPsaYSsw5Cg/cfANk5K4Jr2YsX756xvX11shzqsreWA==`. The installed package metadata independently declares the same exact version. The declaration excerpts establish only the staged `Context.Service`, `Layer.effect`, and `Layer.provide` APIs.

## Portable retrieval and verification

- Exact registry tarball: `https://registry.npmjs.org/effect/-/effect-4.0.0-rc.111.tgz`
- Exact upstream tag: `https://github.com/Effect-TS/effect/tree/effect%404.0.0-rc.111/packages/effect`

Recreate the installed-package fixtures from the registry tarball, then compare the printed SHA-256 values with the table above:

```bash
set -euo pipefail
tmp="$(mktemp -d)"
curl -fsSL https://registry.npmjs.org/effect/-/effect-4.0.0-rc.111.tgz -o "$tmp/effect.tgz"
actual="$(openssl dgst -sha512 -binary "$tmp/effect.tgz" | openssl base64 -A)"
test "$actual" = 'ASd5L58EIR0CUNueZNKKjSsyOCd+2alxOAIaTcHaqkJkPsaYSsw5Cg/cfANk5K4Jr2YsX756xvX11shzqsreWA=='
tar -xzf "$tmp/effect.tgz" -C "$tmp"
cp "$tmp/package/package.json" /tmp/effect-rc111-package.json
sed -n '188,350p' "$tmp/package/dist/Context.d.ts" > /tmp/effect-rc111-context-service.d.ts
sed -n '1131,1210p' "$tmp/package/dist/Layer.d.ts" > /tmp/effect-rc111-layer-effect.d.ts
sed -n '1704,2029p' "$tmp/package/dist/Layer.d.ts" > /tmp/effect-rc111-layer-provide.d.ts
shasum -a 256 /tmp/effect-rc111-*
```

Verify the checked-in payloads without rewriting them:

```bash
shasum -a 256 evals/fp-planning-fixtures/effect-resolved-lock.txt \
  evals/fp-planning-fixtures/effect-rc111-package.json \
  evals/fp-planning-fixtures/effect-rc111-context-service.d.ts \
  evals/fp-planning-fixtures/effect-rc111-layer-effect.d.ts \
  evals/fp-planning-fixtures/effect-rc111-layer-provide.d.ts
```

# Windows Test Release Changelog

## Test build — 2026-10-03 — RX 9060 XT / gfx1200

### Performance path
- Uses the existing Windows async interop path as the K release default.
- Enables batched VRAM input conversion/copies for the K release launcher.
- Enables GPU-ordered D3D12/HIP fence dependencies through the existing async GPU pipeline path.
- Keeps the Windows command-list/resource lifetime guards and cached interop command lists intact.
- Enables the gfx1200 K LDS bank-phase padding candidate by default for builds targeting RX 9060 XT / gfx1200.

### Release cleanup
- Reduced the Windows test launcher surface to exactly three .cmd files: START-K.cmd, START-K-PROFILE.cmd, and RESTORE-GAME.cmd.
- Removed legacy async, fast-K, and M launcher variants from the generated test package.
- Updated PowerShell launch plumbing and diagnostics to carry AsyncGpuPipeline.
- Added this changelog to the test package.

### Deliberately not default
- WGP output-tail placement remains opt-in until a full RX 9060 XT / gfx1200 gameplay A/B validates it.
- Direct output remains opt-in and requires a separately validated local texture-kernel bundle.
- Packed FP16 accumulator and packed-F16 WMMA experiments remain disabled because prior validation did not meet the strict output-preservation gate.
- M/FP8 remains outside the K-focused default path.

### Validation status
- Source baseline: 2a0b9a87dc2fe8c57fe2e7f15a104d781af4990b.
- RX 9060 XT / gfx1200 full gameplay validation: pending user hardware run.
- This release is an experimental performance test, not a universal Windows build.

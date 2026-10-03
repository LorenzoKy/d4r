# Windows Test Release Changelog

## Test build — 2026-10-03 — RX 9060 XT / gfx1200

### Follow-up diagnostic fix
- Restored `START-K.cmd` to the previously validated async+batch combination (`-AsyncInterop -BatchInputCopies`). `LinearInputs`, `DirectOutput`, and `AsyncGpuPipeline` are no longer enabled by the main launcher while we re-establish the known-good baseline.
- `START-K-PROFILE.cmd` mirrors that baseline and adds diagnostics only, so its measurements are directly comparable to the known-good async+batch path.
- Added explicit `D4R_ASYNC_SLOT_WAIT` sampling to expose producer backpressure when all three D3D12 copy slots are still in flight.
- The translated output array→VRAM copy is now queued asynchronously on the GPU default stream when `D4R_ASYNC_GPU_PIPELINE` is active; the output fence is signalled after that copy instead of forcing a host `cuStreamSynchronize`.
- Added first-frame output-path diagnostics so a profile run records whether a native output texture kernel actually enabled direct output.
- Fixed `START-K-PROFILE.cmd`: `-ProfileGpuBoundary` is now accepted by `quick-test.ps1`, forwarded to the Windows runner, and recorded in the diagnostic manifest.
- The next profile run is intended to separate input-fence, NGX evaluation, output handling, and D3D12 boundary time instead of relying on the aggregate `interop_ngx_ms` value.

### Performance path
- Uses the existing Windows GPU-ordered async interop path for the K release default.
- Enables batched VRAM input conversions/copies for the K release launcher.
- Enables the gfx1200 K LDS bank-phase padding candidate by default.
- Keeps the existing Windows command-list/resource lifetime guards and cached interop command lists.
- Uses the existing direct-output and linear-input fast paths already present on the `windows` branch.

### Release cleanup
- Reduced the Windows test launcher surface to exactly three `.cmd` files: `START-K.cmd`, `START-K-PROFILE.cmd`, and `RESTORE-GAME.cmd`.
- Removed legacy optimized/async/M launcher variants from the generated test package.
- Updated PowerShell launch plumbing and diagnostics to carry `AsyncGpuPipeline`.
- This changelog is packaged with every test release.

### Deliberately experimental
- WGP output-tail placement remains opt-in unless validated on RX 9060 XT / gfx1200 hardware.
- Packed FP16 accumulator/WMMA experiments remain disabled because they did not meet the strict output-preservation gate.
- Full RX 9060 XT gameplay/image/performance validation is still a user-hardware step.

### Source
- Baseline requested for the optimization round: `2a0b9a87dc2fe8c57fe2e7f15a104d781af4990b`.
- The final source of this release is the current `windows` branch, including the subsequent Windows Phase 1 synchronization, lifetime, interop, K, and RDNA4 optimizations.

# Examples

## Example 1: Analyze packet-processing latency regressions

Input

```
My VPP plugin's per-packet latency increased after upgrading DPDK. How to debug and fix this in production?
```

Expected output

- Ask about DPDK and kernel versions, NIC/Driver, RSS, hugepage configuration, and any change in PMD.
- Recommend reproducing a minimal test with `pktgen` and capture timestamps, use perf, measure bursts and batching, check for memory alignment and prefetching efficacy.
- Provide code snippets to avoid per-packet malloc on the fast path and show a sample `vpp_plugin_process_batch` C API call.

---

## Example 2: SmartNIC offload integration

Input

```
I want to offload a L4 feature to a SmartNIC while keeping VPP as the control plane. What pitfalls and integration patterns should I follow?
```

Expected output

- Discuss offload consistency, telemetry, failure modes, fallbacks to software path, and configuration synchronization.
- Suggest using opaque handles and concise C API to manage NIC resources from VPP main thread.
- Include pattern for asynchronous completion callbacks and how to expose them safely across the C/C++ boundary.

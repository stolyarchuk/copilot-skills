---
name: doca-expert-examples
description: "Representative prompts and expected outputs for the `doca-expert` skill."
---

# Examples

Input:

```text
How can I implement a high-performance 5-tuple classifier using DOCA Flow in C++ that steers packets to different host RX queues on a BlueField SmartNIC? Include architecture notes and a short C++ example.
```

Expected output:

```text
Summary: Use a DOCA Flow table for 5-tuple matches and use queue-forward actions; program rules in batches.
Checklist:
- Use flow tables for 5-tuple match
- Batch control-plane updates
- Use RAII wrappers for DOCA resources

C++ snippet:

    struct FlowTableHandle { /* create/destroy table */ };
    FlowTableHandle table;
    // add 5-tuple rule -> queue

References:
- DOCA Flow SDK docs: https://docs.nvidia.com/doca/sdk/doca-flow/index.html
- DOCA Flow API (v3.2.0): https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html
```
References:

- [DOCA Flow SDK docs](https://docs.nvidia.com/doca/sdk/doca-flow/index.html)
- [DOCA Flow API (v3.2.0)](https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html)
```

Input:

```text
I'm seeing high tail latency on a DOCA Flow pipeline running on BlueField. What are the likely causes and how to mitigate them? Provide C++-level fixes or patterns.
```

Expected output:

```text
Summary: Tail latency usually from contention or synchronous ops; use lockless handoff and batching.
Checklist:
- Profile queues and CPU
- Use SPSC queues for handoff
- Batch rule updates

C++ snippet:

    // SPSC queue (sketch)
    template <typename T> class SpscQueue { /*...*/ };

References:
- DOCA Flow SDK docs: https://docs.nvidia.com/doca/sdk/doca-flow/index.html
- DOCA Flow API (v3.2.0): https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html
```
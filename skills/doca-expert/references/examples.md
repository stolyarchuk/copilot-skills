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

Input:

```text
How should I manage DOCA device lifecycle and resource cleanup in C++ (open/close, attach/detach, health checks)? Provide an idiomatic RAII example and operational checklist.
```

Expected output:

```text
Summary: Wrap device open/close and attach/detach into an RAII device class that performs deterministic init/cleanup, exposes health probe methods, and converts C-style errors into safe C++ error handling.

Checklist:
- Open the device and verify capabilities before allocating resources.
- Use RAII for device and resource lifetimes and ensure destructors are no-throw.
- Provide explicit health-check and telemetry hooks and a graceful detach path for upgrades.
- Log errors and expose recoverable vs. fatal error categories.

C++ snippet (device RAII):

    // Idiomatic RAII device wrapper (illustrative)
    class DocaDevice {
    public:
        explicit DocaDevice(int dev_index) {
            if (doca_dev_open(dev_index, &dev_) != 0) { throw std::runtime_error("open device"); }
            // query and store capabilities
        }
        ~DocaDevice() noexcept {
            if (dev_) doca_dev_close(dev_); // best-effort cleanup
        }

        bool health_check() const {
            // call a DOCA health API, return boolean
            return true;
        }

    private:
        doca_dev_handle dev_ = nullptr; // C API handle (pseudo-symbol)
    };

References:
- [DOCA Flow SDK docs](https://docs.nvidia.com/doca/sdk/doca-flow/index.html)
- [DOCA Flow API (v3.2.0)](https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html)
```

Input:

```text
What's the recommended approach for batching rule updates to DOCA Flow tables from a C++ control plane? Show a batching pattern and commit model.
```

Expected output:

```text
Summary: Use an append-then-commit batching strategy: accumulate rule updates in memory, validate them, then submit an atomic batch commit to the device to reduce syncs and increase throughput.

Checklist:
- Validate batch size against device/table limits before committing.
- Group related updates (adds/removes) to optimize TCAM usage and avoid thrashing.
- Use retries with exponential backoff for transient commit failures; emit telemetry on commit latency.

C++ snippet (batch updates):

    struct Rule { /* match, action fields */ };

    class BatchUpdater {
    public:
        void add(const Rule& r) { pending_.push_back(r); }
        bool commit() {
            // pseudo-API: doca_flow_table_add_rules_batch
            if (pending_.empty()) return true;
            auto rc = doca_flow_table_add_rules_batch(table_, pending_.data(), pending_.size());
            pending_.clear();
            return rc == 0;
        }

    private:
        std::vector<Rule> pending_;
        doca_table_handle table_ = nullptr;
    };

References:
- [DOCA Flow SDK docs](https://docs.nvidia.com/doca/sdk/doca-flow/index.html)
- [DOCA Flow API (v3.2.0)](https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html)
```

Input:

```text
Provide a larger C++ RAII wrapper example that combines device management and batch rule updates into a safe small class suitable for production use.
```

Expected output:

```text
Summary: Encapsulate device and table lifecycle into a `FlowProgrammer` RAII class that owns a `DocaDevice` and a `BatchUpdater`, exposing a safe API for adding rules and committing batches, while providing telemetry hooks.

Checklist:
- Ensure deterministic cleanup and no-throw destructors.
- Separate validate vs. commit paths and provide async-friendly commit hooks.
- Provide metrics for commit latency, error counts, and table usage.

C++ snippet (FlowProgrammer):

    class FlowProgrammer {
    public:
        explicit FlowProgrammer(int dev_index) : dev_{dev_index}, updater_{/*table*/} {}
        ~FlowProgrammer() noexcept = default; // dev_ and updater_ clean up

        void add_rule(const Rule& r) { updater_.add(r); }

        bool commit_batch() {
            if (!updater_.commit()) {
                // emit telemetry, maybe retry
                return false;
            }
            return true;
        }

    private:
        DocaDevice dev_;
        BatchUpdater updater_;
    };

References:
- [DOCA Flow SDK docs](https://docs.nvidia.com/doca/sdk/doca-flow/index.html)
- [DOCA Flow API (v3.2.0)](https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html)
```References:

- [DOCA Flow SDK docs](https://docs.nvidia.com/doca/sdk/doca-flow/index.html)
- [DOCA Flow API (v3.2.0)](https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html)

```text

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

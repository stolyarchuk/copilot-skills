#!/usr/bin/env python3
"""A minimal mock runner for local testing the doca-expert skill.

Deterministic, short responses used by `validate_examples.py`.
"""

import sys


def run_prompt(s: str) -> str:
    s = s.strip()

    if "5-tuple" in s or "5 tuple" in s:
        return (
            "Summary: Use a DOCA Flow table for 5-tuple matches and use queue-forward actions; program rules in batches.\n\n"
            "Checklist:\n- Use flow tables for 5-tuple match\n- Batch control-plane updates\n- Use RAII wrappers for DOCA resources\n\n"
            "C++ snippet:\n\n"
            "    struct FlowTableHandle { /* create/destroy table */ };\n"
            "    FlowTableHandle table;\n"
            "    // add 5-tuple rule -> queue\n\n"
            "References:\n- DOCA Flow SDK docs: https://docs.nvidia.com/doca/sdk/doca-flow/index.html\n"
            "- DOCA Flow API (v3.2.0): https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html"
        )

    if "tail latency" in s or "high tail" in s:
        return (
            "Summary: Tail latency usually from contention or synchronous ops; use lockless handoff and batching.\n\n"
            "Checklist:\n- Profile queues and CPU\n- Use SPSC queues for handoff\n- Batch rule updates\n\n"
            "C++ snippet:\n\n"
            "    // SPSC queue (sketch)\n"
            "    template <typename T> class SpscQueue { /*...*/ };\n\n"
            "References:\n- DOCA Flow SDK docs: https://docs.nvidia.com/doca/sdk/doca-flow/index.html\n"
            "- DOCA Flow API (v3.2.0): https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html"
        )

    if "device lifecycle" in s or ("device" in s and ("open" in s or "close" in s)):
        return (
            "Summary: Wrap device open/close and attach/detach into an RAII device class that performs deterministic init/cleanup, exposes health probe methods, and converts C-style errors into safe C++ error handling.\n\n"
            "Checklist:\n- Open the device and verify capabilities before allocating resources.\n- Use RAII for device and resource lifetimes and ensure destructors are no-throw.\n- Provide explicit health-check and telemetry hooks and a graceful detach path for upgrades.\n- Log errors and expose recoverable vs. fatal error categories.\n\n"
            "C++ snippet (device RAII):\n\n"
            "    // Idiomatic RAII device wrapper (illustrative)\n"
            "    class DocaDevice {\n"
            "    public:\n"
            "        explicit DocaDevice(int dev_index) {\n"
            "            if (doca_dev_open(dev_index, &dev_) != 0) { throw std::runtime_error(\"open device\"); }\n"
            "            // query and store capabilities\n"
            "        }\n"
            "        ~DocaDevice() noexcept {\n"
            "            if (dev_) doca_dev_close(dev_); // best-effort cleanup\n"
            "        }\n\n"
            "        bool health_check() const {\n"
            "            // call a DOCA health API, return boolean\n"
            "            return true;\n"
            "        }\n\n"
            "    private:\n"
            "        doca_dev_handle dev_ = nullptr; // C API handle (pseudo-symbol)\n"
            "    };\n\n"
            "References:\n- DOCA Flow SDK docs: https://docs.nvidia.com/doca/sdk/doca-flow/index.html\n"
            "- DOCA Flow API (v3.2.0): https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html"
        )

    if "FlowProgrammer" in s or "RAII wrapper" in s or ("combine" in s and "device" in s):
        return (
            "Summary: Encapsulate device and table lifecycle into a `FlowProgrammer` RAII class that owns a `DocaDevice` and a `BatchUpdater`, exposing a safe API for adding rules and committing batches, while providing telemetry hooks.\n\n"
            "Checklist:\n- Ensure deterministic cleanup and no-throw destructors.\n- Separate validate vs. commit paths and provide async-friendly commit hooks.\n- Provide metrics for commit latency, error counts, and table usage.\n\n"
            "C++ snippet (FlowProgrammer):\n\n"
            "    class FlowProgrammer {\n"
            "    public:\n"
            "        explicit FlowProgrammer(int dev_index) : dev_{dev_index}, updater_{/*table*/} {}\n"
            "        ~FlowProgrammer() noexcept = default; // dev_ and updater_ clean up\n\n"
            "        void add_rule(const Rule& r) { updater_.add(r); }\n\n"
            "        bool commit_batch() {\n"
            "            if (!updater_.commit()) {\n"
            "                // emit telemetry, maybe retry\n"
            "                return false;\n"
            "            }\n"
            "            return true;\n"
            "        }\n\n"
            "    private:\n"
            "        DocaDevice dev_;\n"
            "        BatchUpdater updater_;\n"
            "    };\n\n"
            "References:\n- [DOCA Flow SDK docs](https://docs.nvidia.com/doca/sdk/doca-flow/index.html)\n"
            "- [DOCA Flow API (v3.2.0)](https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html)"
        )
    if "batch" in s and ("rule" in s or "batch update" in s or "batch updates" in s):
        return (
            "Summary: Use an append-then-commit batching strategy: accumulate rule updates in memory, validate them, then submit an atomic batch commit to the device to reduce syncs and increase throughput.\n\n"
            "Checklist:\n- Validate batch size against device/table limits before committing.\n- Group related updates (adds/removes) to optimize TCAM usage and avoid thrashing.\n- Use retries with exponential backoff for transient commit failures; emit telemetry on commit latency.\n\n"
            "C++ snippet (batch updates):\n\n"
            "    struct Rule { /* match, action fields */ };\n\n"
            "    class BatchUpdater {\n"
            "    public:\n"
            "        void add(const Rule& r) { pending_.push_back(r); }\n"
            "        bool commit() {\n"
            "            // pseudo-API: doca_flow_table_add_rules_batch\n"
            "            if (pending_.empty()) return true;\n"
            "            auto rc = doca_flow_table_add_rules_batch(table_, pending_.data(), pending_.size());\n"
            "            pending_.clear();\n"
            "            return rc == 0;\n"
            "        }\n\n"
            "    private:\n"
            "        std::vector<Rule> pending_;\n"
            "        doca_table_handle table_ = nullptr;\n"
            "    };\n\n"
            "References:\n- [DOCA Flow SDK docs](https://docs.nvidia.com/doca/sdk/doca-flow/index.html)\n"
            "- [DOCA Flow API (v3.2.0)](https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html)"
        )

    if "FlowProgrammer" in s or "RAII wrapper" in s or ("combine" in s and "device" in s):
        return (
            "Summary: Encapsulate device and table lifecycle into a `FlowProgrammer` RAII class that owns a `DocaDevice` and a `BatchUpdater`, exposing a safe API for adding rules and committing batches, while providing telemetry hooks.\n\n"
            "Checklist:\n- Ensure deterministic cleanup and no-throw destructors.\n- Separate validate vs. commit paths and provide async-friendly commit hooks.\n- Provide metrics for commit latency, error counts, and table usage.\n\n"
            "C++ snippet (FlowProgrammer):\n\n"
            "    class FlowProgrammer {\n"
            "    public:\n"
            "        explicit FlowProgrammer(int dev_index) : dev_{dev_index}, updater_{/*table*/} {}\n"
            "        ~FlowProgrammer() noexcept = default; // dev_ and updater_ clean up\n\n"
            "        void add_rule(const Rule& r) { updater_.add(r); }\n\n"
            "        bool commit_batch() {\n"
            "            if (!updater_.commit()) {\n"
            "                // emit telemetry, maybe retry\n"
            "                return false;\n"
            "            }\n"
            "            return true;\n"
            "        }\n\n"
            "    private:\n"
            "        DocaDevice dev_;\n"
            "        BatchUpdater updater_;\n"
            "    };\n\n"
            "References:\n- DOCA Flow SDK docs: https://docs.nvidia.com/doca/sdk/doca-flow/index.html\n"
            "- DOCA Flow API (v3.2.0): https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html"
        )

    # Default: echo short help sentence
    return "Ask me a DOCA Flow or SmartNIC question (e.g., '5-tuple classifier', 'tail latency')."


if __name__ == "__main__":
    data = sys.stdin.read()
    out = run_prompt(data)
    sys.stdout.write(out)

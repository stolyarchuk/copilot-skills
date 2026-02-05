#!/usr/bin/env python3
"""A minimal mock runner for local testing.

This runner reads stdin and emits deterministic output for the examples in
references/examples.md.

Real deployments should replace this with the real skill runtime.
"""

import sys

EX1_MARKER = "Backend Engineer (Go)"
EX2_MARKER = "Site Reliability Engineer (SRE)"
EX3_MARKER = "C++ R&D Engineer"
EX4_MARKER = "C++ developer (low-latency networking/DPDK)"


def run(text: str) -> str:
    s = text.strip()

    if EX1_MARKER in s:
        return (
            "Adapted resume\n"
            "SUMMARY\n"
            "Backend Engineer (Go) - production Go services with PostgreSQL, gRPC, and Kubernetes deployments.\n"
            "\n"
            "KEY SKILLS\n"
            "- Go (production), gRPC, PostgreSQL\n"
            "- Kubernetes (deployments, debugging)\n"
            "- Redis (nice-to-have)\n"
            "\n"
            "EXPERIENCE\n"
            "Company A - Backend Engineer\n"
            "- Built and shipped Go microservices; delivered API endpoints over gRPC.\n"
            "- Used PostgreSQL in production services (queries, schema changes, performance troubleshooting).\n"
            "- Supported Kubernetes deployments and production debugging.\n"
            "\n"
            "Company B - Developer\n"
            "- Built internal tools in Python.\n"
            "\n"
            "SKILLS\n"
            "Go, PostgreSQL, gRPC, Kubernetes, Redis\n"
            "\n"
            "Best-met requirements\n"
            "- Go in production: Company A role explicitly foregrounds Go microservices.\n"
            "- PostgreSQL: Company A role explicitly foregrounds PostgreSQL usage in production.\n"
            "- gRPC: Company A role explicitly foregrounds gRPC APIs.\n"
            "- Kubernetes: Company A role explicitly foregrounds deployments and debugging.\n"
            "\n"
            "Gaps + how to close\n"
            '- Proof/scope is thin ("built microservices", "worked on APIs"): add concrete scope you already have (service count, ownership, traffic, latency/cost outcomes) without inventing numbers.\n'
            "- Kubernetes depth is vague: clarify what you actually did (helm/kustomize, rollout debugging, logs, resource limits, incident response) if true.\n"
            "- Redis is listed but not evidenced: either add a real bullet where you used it (if true) or remove it from skills to avoid looking padded."
        )

    if EX2_MARKER in s:
        return (
            "Adapted resume\n"
            "SUMMARY\n"
            "Site Reliability Engineer - Linux production ops, Kubernetes troubleshooting, monitoring/alerting, and on-call.\n"
            "\n"
            "KEY SKILLS\n"
            "- Linux (production), incident response, on-call\n"
            "- Kubernetes (operations, troubleshooting)\n"
            "- Prometheus, Grafana\n"
            "- Terraform (nice-to-have)\n"
            "- Python (automation)\n"
            "\n"
            "EXPERIENCE\n"
            "Company A - Platform Engineer\n"
            "- Operated Kubernetes clusters in production, including troubleshooting and reliability support.\n"
            "- Implemented monitoring/alerting with Prometheus and Grafana.\n"
            "- Participated in on-call and incident response.\n"
            "- Wrote Python automation scripts to reduce manual ops work.\n"
            "\n"
            "Company B - Backend Engineer\n"
            "- Built Go microservices.\n"
            "- Worked with PostgreSQL.\n"
            "\n"
            "SKILLS\n"
            "Linux, Kubernetes, Prometheus, Grafana, Terraform, Python, Go, PostgreSQL\n"
            "\n"
            "Best-met requirements\n"
            "- Linux production operations: Summary/skills foreground Linux production ops.\n"
            "- Kubernetes: Company A role explicitly foregrounds cluster operations and troubleshooting.\n"
            "- Monitoring/alerting: Company A role explicitly foregrounds Prometheus/Grafana.\n"
            "- Incident response and on-call: Company A role explicitly foregrounds on-call/incident response.\n"
            "\n"
            "Gaps + how to close\n"
            "- On-call/incident specifics are missing: add what you can truthfully support (rotation, incident types, postmortems, SLOs) without inventing numbers.\n"
            "- Kubernetes depth is still broad: clarify concrete tasks you did (deployments, rollouts, debugging, capacity, upgrades, networking) if true.\n"
            "- Terraform is listed but not evidenced: add a real bullet if you used it, otherwise remove it to avoid looking padded."
        )

    if EX3_MARKER in s:
        return (
            "Adapted resume\n"
            "SUMMARY\n"
            "C++ R&D Engineer - modern C++ on Linux with performance optimization and concurrency.\n"
            "\n"
            "KEY SKILLS\n"
            "- Modern C++ (C++17+), performance optimization\n"
            "- Concurrency (multithreading)\n"
            "- Linux toolchain: CMake, gdb\n"
            "- Networking (nice-to-have)\n"
            "\n"
            "EXPERIENCE\n"
            "Company A - C++ Engineer\n"
            "- Developed modern C++ application on Linux (CMake build, debugging with gdb).\n"
            "- Improved performance through targeted optimization work.\n"
            "- Implemented multithreading/concurrency features.\n"
            "\n"
            "Company B - DevOps Engineer\n"
            "- Managed Kubernetes.\n"
            "- Set up monitoring.\n"
            "\n"
            "SKILLS\n"
            "C++, Linux, CMake, gdb, multithreading, networking\n"
            "\n"
            "Best-met requirements\n"
            "- Modern C++ (C++17+): Resume foregrounds modern C++ and C++ engineering experience.\n"
            "- Performance optimization: Company A role explicitly foregrounds optimization work.\n"
            "- Concurrency: Company A role explicitly foregrounds multithreading.\n"
            "- Linux toolchain: Company A role explicitly foregrounds Linux + CMake + gdb.\n"
            "\n"
            "Gaps + how to close\n"
            "- The achievements are still generic: add concrete problems you solved (latency/throughput, memory footprint, CPU) and what changed, using only facts you already have.\n"
            "- Concurrency depth is unclear: clarify what you built (threading model, synchronization choices, contention issues) if true.\n"
            "- Nice-to-haves are not evidenced: if you have real networking/SIMD work, add a truthful bullet; otherwise keep them out to avoid keyword padding."
        )

    if EX4_MARKER in s:
        return (
            "Adapted resume\n"
            "SUMMARY\n"
            "C++ developer (low-latency networking/DPDK) - packet processing on Linux with DPDK, performance optimization, and concurrency.\n"
            "\n"
            "KEY SKILLS\n"
            "- Modern C++ (C++17+), Linux networking fundamentals\n"
            "- DPDK (packet processing)\n"
            "- Performance profiling/optimization (perf), debugging (gdb)\n"
            "- Concurrency (multithreading)\n"
            "\n"
            "EXPERIENCE\n"
            "Company A - C++ Engineer\n"
            "- Built packet-processing components on Linux using DPDK.\n"
            "- Improved performance via profiling-driven optimization.\n"
            "- Implemented multithreading/concurrency features.\n"
            "\n"
            "Company B - Backend Engineer\n"
            "- Built REST APIs.\n"
            "- Used PostgreSQL.\n"
            "\n"
            "SKILLS\n"
            "C++, Linux, DPDK, networking, multithreading, perf, gdb\n"
            "\n"
            "Best-met requirements\n"
            "- Modern C++ (C++17+): Resume foregrounds C++ engineering experience.\n"
            "- Linux networking fundamentals: Summary/skills foreground networking on Linux.\n"
            "- DPDK: Company A role explicitly foregrounds DPDK packet processing.\n"
            "- Performance profiling/optimization: Company A role explicitly foregrounds profiling-driven optimization.\n"
            "- Concurrency: Company A role explicitly foregrounds multithreading.\n"
            "\n"
            "Gaps + how to close\n"
            "- Low-latency credibility is still thin: add concrete facts you already have (p99 latency, throughput, packet sizes, CPU budget, drop rates) without inventing numbers.\n"
            "- DPDK depth is vague: clarify what you owned (rte_mbuf lifecycle, RX/TX rings, mempools, multi-queue) if true.\n"
            "- Nice-to-haves aren’t evidenced: if you really did RSS/offloads/NUMA/hugepages tuning, add a truthful bullet; otherwise keep them out to avoid keyword padding."
        )

    return s


if __name__ == "__main__":
    data = sys.stdin.read()
    sys.stdout.write(run(data))

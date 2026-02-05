# Examples and Tests

This file contains example prompts and expected outputs to help validate the `cv-adapter` skill.

## Example 1 - Adapt resume to a specific backend role

Input:

```text
Act as a recruiter filling a specific position, not just "looking at resumes in general."
I will provide you the job description: [job description text]
Your task is to:
- adapt the resume to the requirements of this specific job
- place emphasis the way a strong candidate would
- remove or downplay anything that doesn't strengthen the application for this role
- highlight the relevant experience and skills first and foremost.
Rules:
- don't add fabricated experience
- don't rewrite the entire thing if it's not necessary
- the goal is for the recruiter to understand in 20–30 seconds: "this person is a good fit"
At the end, tell me:
- which job requirements the resume now meets best
- where there is still a gap and how it can be closed.

JOB DESCRIPTION
Backend Engineer (Go)
Must-have:
- Go in production
- PostgreSQL
- gRPC
- Kubernetes (deployments, debugging)
Nice-to-have:
- Redis

RESUME
SUMMARY
Software engineer.

EXPERIENCE
Company A - Backend Engineer
- Built microservices.
- Worked on APIs.
- Used Go and PostgreSQL.
- Supported deployments.

Company B - Developer
- Worked on internal tools.
- Used Python.

SKILLS
Go, PostgreSQL, gRPC, Kubernetes, Redis, Photoshop
```

Expected output:

```text
Adapted resume
SUMMARY
Backend Engineer (Go) - production Go services with PostgreSQL, gRPC, and Kubernetes deployments.

KEY SKILLS
- Go (production), gRPC, PostgreSQL
- Kubernetes (deployments, debugging)
- Redis (nice-to-have)

EXPERIENCE
Company A - Backend Engineer
- Built and shipped Go microservices; delivered API endpoints over gRPC.
- Used PostgreSQL in production services (queries, schema changes, performance troubleshooting).
- Supported Kubernetes deployments and production debugging.

Company B - Developer
- Built internal tools in Python.

SKILLS
Go, PostgreSQL, gRPC, Kubernetes, Redis

Best-met requirements
- Go in production: Company A role explicitly foregrounds Go microservices.
- PostgreSQL: Company A role explicitly foregrounds PostgreSQL usage in production.
- gRPC: Company A role explicitly foregrounds gRPC APIs.
- Kubernetes: Company A role explicitly foregrounds deployments and debugging.

Gaps + how to close
- Proof/scope is thin ("built microservices", "worked on APIs"): add concrete scope you already have (service count, ownership, traffic, latency/cost outcomes) without inventing numbers.
- Kubernetes depth is vague: clarify what you actually did (helm/kustomize, rollout debugging, logs, resource limits, incident response) if true.
- Redis is listed but not evidenced: either add a real bullet where you used it (if true) or remove it from skills to avoid looking padded.
```

## Example 2 - Adapt resume to a specific SRE role

Input:

```text
Act as a recruiter filling a specific position, not just "looking at resumes in general."
I will provide you the job description: [job description text]
Your task is to:
- adapt the resume to the requirements of this specific job
- place emphasis the way a strong candidate would
- remove or downplay anything that doesn't strengthen the application for this role
- highlight the relevant experience and skills first and foremost.
Rules:
- don't add fabricated experience
- don't rewrite the entire thing if it's not necessary
- the goal is for the recruiter to understand in 20–30 seconds: "this person is a good fit"
At the end, tell me:
- which job requirements the resume now meets best
- where there is still a gap and how it can be closed.

JOB DESCRIPTION
Site Reliability Engineer (SRE)
Must-have:
- Linux production operations
- Kubernetes (operations, troubleshooting)
- Monitoring/alerting (Prometheus/Grafana)
- Incident response and on-call
Nice-to-have:
- Terraform
- Go or Python

RESUME
SUMMARY
Software engineer.

EXPERIENCE
Company A - Platform Engineer
- Managed Kubernetes clusters.
- Set up monitoring.
- Participated in on-call.
- Wrote automation scripts in Python.

Company B - Backend Engineer
- Built Go microservices.
- Worked with PostgreSQL.

SKILLS
Linux, Kubernetes, Prometheus, Grafana, Terraform, Python, Go, PostgreSQL, Photoshop
```

Expected output:

```text
Adapted resume
SUMMARY
Site Reliability Engineer - Linux production ops, Kubernetes troubleshooting, monitoring/alerting, and on-call.

KEY SKILLS
- Linux (production), incident response, on-call
- Kubernetes (operations, troubleshooting)
- Prometheus, Grafana
- Terraform (nice-to-have)
- Python (automation)

EXPERIENCE
Company A - Platform Engineer
- Operated Kubernetes clusters in production, including troubleshooting and reliability support.
- Implemented monitoring/alerting with Prometheus and Grafana.
- Participated in on-call and incident response.
- Wrote Python automation scripts to reduce manual ops work.

Company B - Backend Engineer
- Built Go microservices.
- Worked with PostgreSQL.

SKILLS
Linux, Kubernetes, Prometheus, Grafana, Terraform, Python, Go, PostgreSQL

Best-met requirements
- Linux production operations: Summary/skills foreground Linux production ops.
- Kubernetes: Company A role explicitly foregrounds cluster operations and troubleshooting.
- Monitoring/alerting: Company A role explicitly foregrounds Prometheus/Grafana.
- Incident response and on-call: Company A role explicitly foregrounds on-call/incident response.

Gaps + how to close
- On-call/incident specifics are missing: add what you can truthfully support (rotation, incident types, postmortems, SLOs) without inventing numbers.
- Kubernetes depth is still broad: clarify concrete tasks you did (deployments, rollouts, debugging, capacity, upgrades, networking) if true.
- Terraform is listed but not evidenced: add a real bullet if you used it, otherwise remove it to avoid looking padded.
```

## Example 3 - Adapt resume to a specific C++ R&D role

Input:

```text
Act as a recruiter filling a specific position, not just "looking at resumes in general."
I will provide you the job description: [job description text]
Your task is to:
- adapt the resume to the requirements of this specific job
- place emphasis the way a strong candidate would
- remove or downplay anything that doesn't strengthen the application for this role
- highlight the relevant experience and skills first and foremost.
Rules:
- don't add fabricated experience
- don't rewrite the entire thing if it's not necessary
- the goal is for the recruiter to understand in 20–30 seconds: "this person is a good fit"
At the end, tell me:
- which job requirements the resume now meets best
- where there is still a gap and how it can be closed.

JOB DESCRIPTION
C++ R&D Engineer
Must-have:
- Modern C++ (C++17+)
- Performance optimization
- Concurrency (threads, lock-free basics)
- Linux toolchain (CMake, gdb)
Nice-to-have:
- Networking
- SIMD

RESUME
SUMMARY
Software engineer.

EXPERIENCE
Company A - C++ Engineer
- Developed a C++ application.
- Optimized performance.
- Worked on multithreading.
- Built with CMake on Linux.

Company B - DevOps Engineer
- Managed Kubernetes.
- Set up monitoring.

SKILLS
C++, Linux, CMake, gdb, multithreading, networking, Kubernetes, Prometheus, Photoshop
```

Expected output:

```text
Adapted resume
SUMMARY
C++ R&D Engineer - modern C++ on Linux with performance optimization and concurrency.

KEY SKILLS
- Modern C++ (C++17+), performance optimization
- Concurrency (multithreading)
- Linux toolchain: CMake, gdb
- Networking (nice-to-have)

EXPERIENCE
Company A - C++ Engineer
- Developed modern C++ application on Linux (CMake build, debugging with gdb).
- Improved performance through targeted optimization work.
- Implemented multithreading/concurrency features.

Company B - DevOps Engineer
- Managed Kubernetes.
- Set up monitoring.

SKILLS
C++, Linux, CMake, gdb, multithreading, networking

Best-met requirements
- Modern C++ (C++17+): Resume foregrounds modern C++ and C++ engineering experience.
- Performance optimization: Company A role explicitly foregrounds optimization work.
- Concurrency: Company A role explicitly foregrounds multithreading.
- Linux toolchain: Company A role explicitly foregrounds Linux + CMake + gdb.

Gaps + how to close
- The achievements are still generic: add concrete problems you solved (latency/throughput, memory footprint, CPU) and what changed, using only facts you already have.
- Concurrency depth is unclear: clarify what you built (threading model, synchronization choices, contention issues) if true.
- Nice-to-haves are not evidenced: if you have real networking/SIMD work, add a truthful bullet; otherwise keep them out to avoid keyword padding.
```

## Example 4 - Adapt resume to a low-latency C++ networking/DPDK role

Input:

```text
Act as a recruiter filling a specific position, not just "looking at resumes in general."
I will provide you the job description: [job description text]
Your task is to:
- adapt the resume to the requirements of this specific job
- place emphasis the way a strong candidate would
- remove or downplay anything that doesn't strengthen the application for this role
- highlight the relevant experience and skills first and foremost.
Rules:
- don't add fabricated experience
- don't rewrite the entire thing if it's not necessary
- the goal is for the recruiter to understand in 20–30 seconds: "this person is a good fit"
At the end, tell me:
- which job requirements the resume now meets best
- where there is still a gap and how it can be closed.

JOB DESCRIPTION
C++ developer (low-latency networking/DPDK)
Must-have:
- Modern C++ (C++17+)
- Linux networking fundamentals
- DPDK (packet processing)
- Performance profiling/optimization
- Concurrency
Nice-to-have:
- NIC offloads / RSS
- NUMA/hugepages tuning

RESUME
SUMMARY
Software engineer.

EXPERIENCE
Company A - C++ Engineer
- Worked on a packet processing application.
- Used DPDK.
- Optimized performance.
- Worked on multithreading.

Company B - Backend Engineer
- Built REST APIs.
- Used PostgreSQL.

SKILLS
C++, Linux, DPDK, networking, multithreading, perf, gdb, Kubernetes, Photoshop
```

Expected output:

```text
Adapted resume
SUMMARY
C++ developer (low-latency networking/DPDK) - packet processing on Linux with DPDK, performance optimization, and concurrency.

KEY SKILLS
- Modern C++ (C++17+), Linux networking fundamentals
- DPDK (packet processing)
- Performance profiling/optimization (perf), debugging (gdb)
- Concurrency (multithreading)

EXPERIENCE
Company A - C++ Engineer
- Built packet-processing components on Linux using DPDK.
- Improved performance via profiling-driven optimization.
- Implemented multithreading/concurrency features.

Company B - Backend Engineer
- Built REST APIs.
- Used PostgreSQL.

SKILLS
C++, Linux, DPDK, networking, multithreading, perf, gdb

Best-met requirements
- Modern C++ (C++17+): Resume foregrounds C++ engineering experience.
- Linux networking fundamentals: Summary/skills foreground networking on Linux.
- DPDK: Company A role explicitly foregrounds DPDK packet processing.
- Performance profiling/optimization: Company A role explicitly foregrounds profiling-driven optimization.
- Concurrency: Company A role explicitly foregrounds multithreading.

Gaps + how to close
- Low-latency credibility is still thin: add concrete facts you already have (p99 latency, throughput, packet sizes, CPU budget, drop rates) without inventing numbers.
- DPDK depth is vague: clarify what you owned (rte_mbuf lifecycle, RX/TX rings, mempools, multi-queue) if true.
- Nice-to-haves aren’t evidenced: if you really did RSS/offloads/NUMA/hugepages tuning, add a truthful bullet; otherwise keep them out to avoid keyword padding.
```

### Running the smoke tests

```bash
python scripts/validate_examples.py --examples references/examples.md --runner "python scripts/mock_runner.py"
```

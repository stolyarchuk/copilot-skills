#!/usr/bin/env python3
"""Minimal mock runner for `cpp-modernize` examples.

It applies a small, deterministic transformation to input examples for smoke tests.
"""

import sys


def standard_response(
    assessment: str,
    recommended_change: str,
    code: str,
    why: str,
    trade_offs: str,
    when_not: str,
    references: str,
) -> str:
    return (
        f"Assessment: {assessment}\n\n"
        f"Recommended change: {recommended_change}\n\n"
        f"Code:\n\n{code}\n\n"
        f"Why: {why}\n\n"
        f"Trade-offs: {trade_offs}\n\n"
        f"When not to do this: {when_not}\n\n"
        f"References: {references}"
    )


def compact_response(
    assessment: str,
    recommended_change: str,
    why: str,
    trade_offs: str,
    boundary_label: str,
    boundary_code: str,
    references: str,
) -> str:
    return (
        f"Assessment: {assessment}\n\n"
        f"Recommended change: {recommended_change}\n\n"
        f"Why: {why}\n\n"
        f"Trade-offs: {trade_offs}\n\n"
        f"{boundary_label}:\n\n{boundary_code}\n\n"
        f"References: {references}"
    )


def modernize_text(s: str) -> str:
    s = s.strip()

    if "concatenates C strings with `strcat` and a fixed buffer" in s:
        return standard_response(
            "The production risk is fixed-buffer overflow and manual C-string handling in code that also needs to preserve delimiter behavior.",
            "Replace the raw buffer logic with `std::string` plus `std::string_view`, while keeping the comma-separator rule explicit.",
            "    #include <span>\n"
            "    #include <string>\n"
            "    #include <string_view>\n"
            "    #include <iostream>\n\n"
            "    void join(std::span<const std::string_view> parts) {\n"
            "        std::string out;\n"
            "        for (size_t i = 0; i < parts.size(); ++i) {\n"
            "            if (i != 0) out += ',';\n"
            "            out += parts[i];\n"
            "        }\n"
            "        std::cout << out << '\\n';\n"
            "    }",
            "This removes unsafe buffer management and keeps the existing output contract obvious in the code.",
            "The result may allocate dynamically, so this is safer and clearer but not a drop-in choice for extremely allocation-sensitive paths.",
            "Do not switch the interface if this function is part of a C or ABI-stable boundary that cannot adopt `std::span` and `std::string_view` yet.",
            "[cppreference - std::basic_string](https://en.cppreference.com/w/cpp/string/basic_string)",
        )

    if "for (size_t i = 0; i < n; ++i) v.push_back(arr[i]);" in s:
        return standard_response(
            "The production risk is manual extent handling and repeated `push_back` growth when the code is really just copying a contiguous range.",
            "Use a non-owning `std::span` plus direct vector construction so the copy intent is explicit.",
            "    #include <span>\n"
            "    #include <vector>\n\n"
            "    void copy(std::span<const int> arr) {\n"
            "        std::vector<int> v(arr.begin(), arr.end());\n"
            "    }",
            "This expresses the non-owning input range directly and removes a hand-written loop that adds no business logic.",
            "Changing the signature to `std::span` affects callers, so this is easiest when the boundary is internal C++ code.",
            "Do not prefer the signature change on a C-facing or ABI-sensitive boundary without a compatibility plan.",
            "[cppreference - std::span](https://en.cppreference.com/w/cpp/container/span)",
        )

    if (
        "Modernize this function that takes a pointer and length into a safer interface"
        in s
    ):
        return standard_response(
            "The production risk is pointer-plus-length drift, where size and data can get out of sync at call sites.",
            "Replace the pair with `std::span<const int>` for a clearer non-owning range contract.",
            "    #include <span>\n\n"
            "    void process(std::span<const int> data) {\n"
            "        for (int value : data) handle(value);\n"
            "    }",
            "`std::span` keeps the extent attached to the data view and makes the interface easier to use correctly.",
            "This improves safety and readability, but requires callers to build with a standard library that supports `std::span`.",
            "Do not change the signature directly if null pointers, sentinel values, or C ABI compatibility are part of the existing contract.",
            "[cppreference - std::span](https://en.cppreference.com/w/cpp/container/span)",
        )

    if "Suggest a modern return type for this function that uses an out-parameter" in s:
        return standard_response(
            "The production risk is losing error detail and forcing callers to coordinate a `bool` with an out-parameter.",
            "Return `std::expected<Config, Error>` if your toolchain and error-handling policy already support it.",
            "    #include <expected>\n"
            "    #include <string>\n\n"
            "    struct Error {\n"
            "        int code;\n"
            "        std::string message;\n"
            "    };\n\n"
            "    std::expected<Config, Error> load_config() {\n"
            "        if (!file_exists()) {\n"
            '            return std::unexpected(Error{1, "file missing"});\n'
            "        }\n"
            "        return Config{/*...*/};\n"
            "    }",
            "This makes success and failure part of the type and removes the awkward split between return value and output object.",
            "`std::expected` adoption depends on library support and can require a broader migration strategy if the codebase is still built around status codes.",
            "Do not push `std::expected` into exception-disabled, C-facing, or older-toolchain code without checking support and compatibility first.",
            "[cppreference - std::expected](https://en.cppreference.com/w/cpp/utility/expected)",
        )

    if "snprintf" in s:
        return standard_response(
            "The production risk is manual buffer sizing and format-string maintenance in code that is really constructing a typed string.",
            "Use `std::format` if the project has the needed library support and this path is not constrained by formatter availability.",
            "    #include <cstdio>\n"
            "    #include <format>\n\n"
            '    auto s = std::format("user={} id={}", name, id);\n'
            "    std::puts(s.c_str());",
            "`std::format` gives type-safe formatting and removes manual buffer management.",
            "Some standard-library implementations lagged on `std::format`, so toolchain support and rollout constraints matter.",
            "Do not switch just for style if you need maximum portability across older compilers or this hot path cannot afford formatter overhead.",
            "[cppreference - std::format](https://en.cppreference.com/w/cpp/utility/format)",
        )

    if "coroutine-based producer" in s or "co_yield" in s:
        return standard_response(
            "The production risk is recommending coroutines without checking compiler support, runtime model, and debugging cost.",
            "Use a minimal coroutine generator only if the codebase already supports coroutine adoption and the extra machinery is justified.",
            "    #include <coroutine>\n"
            "    #include <optional>\n\n"
            "    struct generator {\n"
            "        struct promise_type {\n"
            "            std::optional<int> value_;\n"
            "            generator get_return_object() {\n"
            "                return generator{std::coroutine_handle<promise_type>::from_promise(*this)};\n"
            "            }\n"
            "            std::suspend_always initial_suspend() { return {}; }\n"
            "            std::suspend_always final_suspend() noexcept { return {}; }\n"
            "            std::suspend_always yield_value(int v) {\n"
            "                value_ = v;\n"
            "                return {};\n"
            "            }\n"
            "            void return_void() {}\n"
            "            void unhandled_exception() { std::terminate(); }\n"
            "        };\n\n"
            "        std::coroutine_handle<promise_type> h_;\n\n"
            "        explicit generator(std::coroutine_handle<promise_type> h) : h_(h) {}\n"
            "        generator(const generator&) = delete;\n"
            "        generator& operator=(const generator&) = delete;\n"
            "        generator(generator&& other) noexcept : h_(other.h_) { other.h_ = {}; }\n"
            "        generator& operator=(generator&& other) noexcept {\n"
            "            if (this != &other) {\n"
            "                if (h_) h_.destroy();\n"
            "                h_ = other.h_;\n"
            "                other.h_ = {};\n"
            "            }\n"
            "            return *this;\n"
            "        }\n"
            "        ~generator() { if (h_) h_.destroy(); }\n\n"
            "        std::optional<int> next() {\n"
            "            if (!h_ || h_.done()) return std::nullopt;\n"
            "            h_.resume();\n"
            "            if (h_.done()) return std::nullopt;\n"
            "            return h_.promise().value_;\n"
            "        }\n"
            "    };\n\n"
            "    generator counter() {\n"
            "        for (int i = 0; i < 3; ++i) co_yield i;\n"
            "    };",
            "Coroutines can express lazy production cleanly, but they should be adopted as a deliberate architectural choice rather than a reflex modernization step.",
            "Coroutine code can be harder to debug and depends on compiler and library support that may not be uniform across your targets.",
            "Do not recommend coroutines in codebases that lack stable support, clear ownership of the coroutine frame, or team familiarity with the execution model.",
            "[cppreference - coroutines](https://en.cppreference.com/w/cpp/language/coroutines)",
        )

    if "Incrementable" in s or "concept" in s:
        return standard_response(
            "The production risk is unconstrained templates that produce poor diagnostics and allow unintended instantiations.",
            "Use a named concept to make the requirement explicit at the call boundary.",
            "    template<typename T>\n"
            "    concept Incrementable = requires(T value) { ++value; };\n\n"
            "    template<Incrementable T>\n"
            "    T inc(T x) {\n"
            "        ++x;\n"
            "        return x;\n"
            "    }",
            "Concepts make template contracts readable and usually improve compiler diagnostics for invalid callers.",
            "This requires C++20+ language support and may be unnecessary for very small local templates with obvious use sites.",
            "Do not add concepts mechanically if the code is stuck on an older standard or the extra abstraction obscures a simpler concrete overload set.",
            "[cppreference - constraints and concepts](https://en.cppreference.com/w/cpp/language/constraints)",
        )

    if "Rewrite this using a ranges pipeline with filter and transform" in s:
        return standard_response(
            "The production risk is overusing pipelines where lifetime or profiling constraints are unclear, but this example is a straightforward pure transform.",
            "Use a `std::views::filter` plus `std::views::transform` pipeline if the codebase already accepts ranges and the data-flow stays simple.",
            "    #include <ranges>\n\n"
            "    auto evens_doubled = in\n"
            "        | std::views::filter([](int v) { return v % 2 == 0; })\n"
            "        | std::views::transform([](int v) { return v * 2; });\n\n"
            "    for (int v : evens_doubled) process(v);",
            "This makes the filter-then-transform intent explicit and composes well when the pipeline stays local and readable.",
            "Ranges can be harder to debug and may not be the best fit for hot loops or lifetime-sensitive pipelines.",
            "Do not prefer the pipeline if the loop is performance-critical, side-effect-heavy, or difficult to reason about with lazy views.",
            "[cppreference - ranges](https://en.cppreference.com/w/cpp/ranges)",
        )

    if "advanced `std::format` example" in s or "padded float and hex formatting" in s:
        return standard_response(
            "The production risk is writing dense formatting logic without checking whether the project can rely on `std::format` across all targets.",
            "Use `std::format` specifiers for width, precision, and hexadecimal output if your standard library support is in place.",
            "    #include <cstdio>\n"
            "    #include <format>\n\n"
            '    auto s = std::format("{:<10} id={:04X} val={:8.2f}", name, id, val);\n'
            "    std::puts(s.c_str());",
            "`std::format` keeps advanced formatting readable without manual buffer sizing or brittle format-string argument ordering.",
            "Formatter support has been uneven across toolchains, so portability and binary size may matter.",
            "Do not adopt `std::format` blindly in portability-sensitive or hot formatting paths without checking support and cost.",
            "[cppreference - std::format](https://en.cppreference.com/w/cpp/utility/format)",
        )

    if "caller docs do not say whether the callee owns them" in s:
        return standard_response(
            "The production risk is ambiguous ownership and lifetime; changing this blindly could introduce leaks, double deletes, or dangling access.",
            "Do not replace the raw pointer with a smart pointer yet. First document whether `set_buffer` observes, borrows, or takes ownership, then modernize to separate observer and owner APIs if needed.",
            "    class Consumer {\n"
            "    public:\n"
            "        void set_buffer(Buffer* buffer) noexcept { buffer_ = buffer; }\n"
            "    private:\n"
            "        Buffer* buffer_ = nullptr; // observer only after ownership is clarified\n"
            "    };",
            "Ownership clarity is the first modernization step; once that contract is explicit, you can choose references, `std::span`, or smart pointers without guessing.",
            "This keeps the legacy pointer storage for now and requires follow-up documentation work before a full API cleanup.",
            "Do not use the observer-style rewrite if the function actually transfers ownership or accepts null as a meaningful state.",
            "[cppreference - std::unique_ptr](https://en.cppreference.com/w/cpp/memory/unique_ptr)",
        )

    if "public shared-library API used by third parties" in s:
        return compact_response(
            "The production risk is ABI breakage for downstream binaries if you change the exported signature to standard-library types.",
            "Keep the boundary stable and modernize internally first; only add a new C++23-facing overload if you can version the API and coordinate rebuilds.",
            "`std::string_view` and `std::expected` can improve clarity, but exported shared-library interfaces need compatibility planning, not blanket modernization.",
            "Preserving the old signature keeps compatibility but means you carry an adapter layer and may not expose the nicest C++23 API immediately.",
            "No code change at boundary",
            "    bool parse_name(const char* input, Result* out) {\n"
            '        auto view = std::string_view(input ? input : "");\n'
            "        return parse_name_impl(view, *out);\n"
            "    }",
            "[cppreference - std::string_view](https://en.cppreference.com/w/cpp/string/basic_string_view)",
        )

    if "We compile with exceptions disabled" in s:
        return standard_response(
            "The production risk is recommending an exception-oriented or poorly supported result type in a build that explicitly disables exceptions.",
            "Keep the non-throwing policy explicit and return a small status object or enum-based result instead of jumping straight to `std::expected`.",
            "    enum class load_config_status {\n"
            "        ok,\n"
            "        file_missing,\n"
            "        parse_error,\n"
            "    };\n\n"
            "    struct load_config_result {\n"
            "        load_config_status status;\n"
            "        Config value;\n"
            "    };\n\n"
            "    load_config_result load_config();",
            "This removes the out-parameter while staying compatible with exception-disabled builds and mixed toolchains.",
            "A custom result type is more verbose than `std::expected` and needs local conventions for checking success.",
            "Do not prefer the custom result wrapper if the codebase already standardizes on `std::expected` and your library support is confirmed.",
            "[cppreference - std::expected](https://en.cppreference.com/w/cpp/utility/expected)",
        )

    if "packet-processing hot path" in s:
        return standard_response(
            "The production risk is adding iterator-adapter overhead or harder-to-profile control flow in a hot path where branch cost and allocation behavior matter.",
            "Keep the conventional loop shape, but reserve output capacity and make the intent explicit instead of forcing a ranges pipeline.",
            "    out.reserve(n);\n"
            "    for (size_t i = 0; i < n; ++i) {\n"
            "        if ((values[i] & mask) != 0) {\n"
            "            out.push_back(values[i] * scale);\n"
            "        }\n"
            "    }",
            "The indexed loop is direct, easy to profile, and less likely to hide temporary objects or view-lifetime issues in allocator-sensitive code.",
            "You keep a manual loop and give up some compositional style compared with `views::filter` and `views::transform`.",
            "Do not keep the hand-written loop by default if profiling shows the code is not hot and a range pipeline materially improves readability without regression.",
            "[cppreference - ranges](https://en.cppreference.com/w/cpp/ranges)",
        )

    if "used by multiple threads" in s:
        return standard_response(
            "The production risk is changing thread-safety or wake-up assumptions in code that already has concurrency-sensitive shared state.",
            "Replace the busy-wait loop with an explicit `std::condition_variable`-based handoff so synchronization stays correct and visible.",
            "    std::unique_lock lock(mutex_);\n"
            "    cv_.wait(lock, [&] { return done_ || ready_; });\n"
            "    if (done_) return;\n"
            "    auto item = item_;\n"
            "    ready_ = false;\n"
            "    lock.unlock();\n"
            "    consume(item);",
            "This removes spinning and makes the coordination contract explicit without inventing a racy lock-free rewrite.",
            "Blocking synchronization is more intrusive than a cosmetic cleanup and requires the producer side to notify the condition variable correctly.",
            "Do not switch to this pattern blindly if the queue already depends on a lock-free design or specific latency behavior that must be preserved.",
            "[cppreference - std::condition_variable](https://en.cppreference.com/w/cpp/thread/condition_variable)",
        )

    if "called from C code in a plugin boundary" in s:
        return compact_response(
            "The production risk is breaking the C ABI and foreign-call expectations by exposing C++ library types at a C plugin boundary.",
            "Keep the exported C signature as-is and modernize only inside the implementation with `std::span` and internal C++ result handling.",
            "C interop boundaries should stay plain and stable; safer C++23 types belong behind the adapter layer unless every caller can move with you.",
            "You keep the older signature and some conversion code, but you avoid ABI churn across plugin or language boundaries.",
            "Internal-only example",
            '    extern "C" int parse_packet(const uint8_t* data, size_t len, Packet* out) {\n'
            "        return parse_packet_impl(\n"
            "            std::span<const std::byte>(reinterpret_cast<const std::byte*>(data), len),\n"
            "            out);\n"
            "    }",
            "[cppreference - std::span](https://en.cppreference.com/w/cpp/container/span)",
        )

    if "Should I rewrite this into a ranges pipeline?" in s and "log_ready" in s:
        return standard_response(
            "The production risk is making a simple side-effecting loop harder to debug by hiding control flow inside a pipeline.",
            "Keep the conventional loop; this is already clear production code, and a ranges pipeline is not a free readability upgrade.",
            "    for (const auto& msg : messages) {\n"
            "        if (!msg.enabled()) continue;\n"
            "        log_ready(msg.id(), msg.payload());\n"
            "    }",
            "For side effects and early-continue logic, the loop is direct and avoids view lifetime questions or extra adaptor noise.",
            "You give up a more declarative style and some composability if the processing later grows into a reusable pure transformation pipeline.",
            "Do not keep the manual loop if the code evolves into a pure filter/transform pipeline with no side effects and clear lifetime boundaries.",
            "[cppreference - std::ranges::filter_view](https://en.cppreference.com/w/cpp/ranges/filter_view)",
        )

    return s


if __name__ == "__main__":
    data = sys.stdin.read()
    out = modernize_text(data)
    sys.stdout.write(out)

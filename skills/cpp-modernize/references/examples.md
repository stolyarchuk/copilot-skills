# Examples

Input:

```text
Modernize this function that concatenates C strings with `strcat` and a fixed buffer.

void join(const char** parts, size_t count) {
    char buf[1024];
    buf[0] = '\0';
    for (size_t i = 0; i < count; ++i) {
        strcat(buf, parts[i]);
        if (i + 1 < count) strcat(buf, ",");
    }
    puts(buf);
}
```

Expected output:

```text
Assessment: The production risk is fixed-buffer overflow and manual C-string handling in code that also needs to preserve delimiter behavior.

Recommended change: Replace the raw buffer logic with `std::string` plus `std::string_view`, while keeping the comma-separator rule explicit.

Code:

    #include <span>
    #include <string>
    #include <string_view>
    #include <iostream>

    void join(std::span<const std::string_view> parts) {
        std::string out;
        for (size_t i = 0; i < parts.size(); ++i) {
            if (i != 0) out += ',';
            out += parts[i];
        }
        std::cout << out << '\n';
    }

Why: This removes unsafe buffer management and keeps the existing output contract obvious in the code.

Trade-offs: The result may allocate dynamically, so this is safer and clearer but not a drop-in choice for extremely allocation-sensitive paths.

When not to do this: Do not switch the interface if this function is part of a C or ABI-stable boundary that cannot adopt `std::span` and `std::string_view` yet.

References: [cppreference - std::basic_string](https://en.cppreference.com/w/cpp/string/basic_string)
```

Input:

```text
Suggest a replacement for this C-style loop that copies into a std::vector:

void copy(const int* arr, size_t n) {
    std::vector<int> v;
    for (size_t i = 0; i < n; ++i) v.push_back(arr[i]);
}
```

Expected output:

```text
Assessment: The production risk is manual extent handling and repeated `push_back` growth when the code is really just copying a contiguous range.

Recommended change: Use a non-owning `std::span` plus direct vector construction so the copy intent is explicit.

Code:

    #include <span>
    #include <vector>

    void copy(std::span<const int> arr) {
        std::vector<int> v(arr.begin(), arr.end());
    }

Why: This expresses the non-owning input range directly and removes a hand-written loop that adds no business logic.

Trade-offs: Changing the signature to `std::span` affects callers, so this is easiest when the boundary is internal C++ code.

When not to do this: Do not prefer the signature change on a C-facing or ABI-sensitive boundary without a compatibility plan.

References: [cppreference - std::span](https://en.cppreference.com/w/cpp/container/span)
```

Input:

```text
Modernize this function that takes a pointer and length into a safer interface:

void process(const int* data, size_t n) {
    for (size_t i = 0; i < n; ++i) handle(data[i]);
}
```

Expected output:

```text
Assessment: The production risk is pointer-plus-length drift, where size and data can get out of sync at call sites.

Recommended change: Replace the pair with `std::span<const int>` for a clearer non-owning range contract.

Code:

    #include <span>

    void process(std::span<const int> data) {
        for (int value : data) handle(value);
    }

Why: `std::span` keeps the extent attached to the data view and makes the interface easier to use correctly.

Trade-offs: This improves safety and readability, but requires callers to build with a standard library that supports `std::span`.

When not to do this: Do not change the signature directly if null pointers, sentinel values, or C ABI compatibility are part of the existing contract.

References: [cppreference - std::span](https://en.cppreference.com/w/cpp/container/span)
```

Input:

```text
Suggest a modern return type for this function that uses an out-parameter and a bool success return:

bool load_config(Config& out) {
    if (!file_exists()) return false;
    out = ...; // load config
    return true;
}
```

Expected output:

```text
Assessment: The production risk is losing error detail and forcing callers to coordinate a `bool` with an out-parameter.

Recommended change: Return `std::expected<Config, Error>` if your toolchain and error-handling policy already support it.

Code:

    #include <expected>
    #include <string>

    struct Error {
        int code;
        std::string message;
    };

    std::expected<Config, Error> load_config() {
        if (!file_exists()) {
            return std::unexpected(Error{1, "file missing"});
        }
        return Config{/*...*/};
    }

Why: This makes success and failure part of the type and removes the awkward split between return value and output object.

Trade-offs: `std::expected` adoption depends on library support and can require a broader migration strategy if the codebase is still built around status codes.

When not to do this: Do not push `std::expected` into exception-disabled, C-facing, or older-toolchain code without checking support and compatibility first.

References: [cppreference - std::expected](https://en.cppreference.com/w/cpp/utility/expected)
```

Input:

```text
Replace this snprintf usage with a modern alternative:

char buf[128];
snprintf(buf, sizeof buf, "user=%s id=%d", name, id);
puts(buf);
```

Expected output:

```text
Assessment: The production risk is manual buffer sizing and format-string maintenance in code that is really constructing a typed string.

Recommended change: Use `std::format` if the project has the needed library support and this path is not constrained by formatter availability.

Code:

    #include <cstdio>
    #include <format>

    auto s = std::format("user={} id={}", name, id);
    std::puts(s.c_str());

Why: `std::format` gives type-safe formatting and removes manual buffer management.

Trade-offs: Some standard-library implementations lagged on `std::format`, so toolchain support and rollout constraints matter.

When not to do this: Do not switch just for style if you need maximum portability across older compilers or this hot path cannot afford formatter overhead.

References: [cppreference - std::format](https://en.cppreference.com/w/cpp/utility/format)
```

Input:

```text
Show a simple coroutine-based producer that yields integers lazily.

/* Show a minimal generator-like coroutine */
// generator<int> counter() { for (int i = 0; i < 3; ++i) co_yield i; }
```

Expected output:

```text
Assessment: The production risk is recommending coroutines without checking compiler support, runtime model, and debugging cost.

Recommended change: Use a minimal coroutine generator only if the codebase already supports coroutine adoption and the extra machinery is justified.

Code:

    #include <coroutine>
    #include <optional>

    struct generator {
        struct promise_type {
            std::optional<int> value_;
            generator get_return_object() {
                return generator{std::coroutine_handle<promise_type>::from_promise(*this)};
            }
            std::suspend_always initial_suspend() { return {}; }
            std::suspend_always final_suspend() noexcept { return {}; }
            std::suspend_always yield_value(int v) {
                value_ = v;
                return {};
            }
            void return_void() {}
            void unhandled_exception() { std::terminate(); }
        };

        std::coroutine_handle<promise_type> h_;

        explicit generator(std::coroutine_handle<promise_type> h) : h_(h) {}
        generator(const generator&) = delete;
        generator& operator=(const generator&) = delete;
        generator(generator&& other) noexcept : h_(other.h_) { other.h_ = {}; }
        generator& operator=(generator&& other) noexcept {
            if (this != &other) {
                if (h_) h_.destroy();
                h_ = other.h_;
                other.h_ = {};
            }
            return *this;
        }
        ~generator() { if (h_) h_.destroy(); }

        std::optional<int> next() {
            if (!h_ || h_.done()) return std::nullopt;
            h_.resume();
            if (h_.done()) return std::nullopt;
            return h_.promise().value_;
        }
    };

    generator counter() {
        for (int i = 0; i < 3; ++i) co_yield i;
    };

Why: Coroutines can express lazy production cleanly, but they should be adopted as a deliberate architectural choice rather than a reflex modernization step.

Trade-offs: Coroutine code can be harder to debug and depends on compiler and library support that may not be uniform across your targets.

When not to do this: Do not recommend coroutines in codebases that lack stable support, clear ownership of the coroutine frame, or team familiarity with the execution model.

References: [cppreference - coroutines](https://en.cppreference.com/w/cpp/language/coroutines)
```

Input:

```text
Show how to use Concepts to constrain templates, e.g., an Incrementable concept.

template<typename T> concept Incrementable = requires(T a) { ++a; };
```

Expected output:

```text
Assessment: The production risk is unconstrained templates that produce poor diagnostics and allow unintended instantiations.

Recommended change: Use a named concept to make the requirement explicit at the call boundary.

Code:

    template<typename T>
    concept Incrementable = requires(T value) { ++value; };

    template<Incrementable T>
    T inc(T x) {
        ++x;
        return x;
    }

Why: Concepts make template contracts readable and usually improve compiler diagnostics for invalid callers.

Trade-offs: This requires C++20+ language support and may be unnecessary for very small local templates with obvious use sites.

When not to do this: Do not add concepts mechanically if the code is stuck on an older standard or the extra abstraction obscures a simpler concrete overload set.

References: [cppreference - constraints and concepts](https://en.cppreference.com/w/cpp/language/constraints)
```

Input:

```text
Rewrite this using a ranges pipeline with filter and transform:

std::vector<int> in = ...; std::vector<int> out; for (int v : in) if (v%2==0) out.push_back(v*2);
```

Expected output:

```text
Assessment: The production risk is overusing pipelines where lifetime or profiling constraints are unclear, but this example is a straightforward pure transform.

Recommended change: Use a `std::views::filter` plus `std::views::transform` pipeline if the codebase already accepts ranges and the data-flow stays simple.

Code:

    #include <ranges>

    auto evens_doubled = in
        | std::views::filter([](int v) { return v % 2 == 0; })
        | std::views::transform([](int v) { return v * 2; });

    for (int v : evens_doubled) process(v);

Why: This makes the filter-then-transform intent explicit and composes well when the pipeline stays local and readable.

Trade-offs: Ranges can be harder to debug and may not be the best fit for hot loops or lifetime-sensitive pipelines.

When not to do this: Do not prefer the pipeline if the loop is performance-critical, side-effect-heavy, or difficult to reason about with lazy views.

References: [cppreference - ranges](https://en.cppreference.com/w/cpp/ranges)
```

Input:

```text
Show an advanced `std::format` example: padded float and hex formatting.

float val = 3.14159; int id = 255; std::string name = "bob";
```

Expected output:

```text
Assessment: The production risk is writing dense formatting logic without checking whether the project can rely on `std::format` across all targets.

Recommended change: Use `std::format` specifiers for width, precision, and hexadecimal output if your standard library support is in place.

Code:

    #include <cstdio>
    #include <format>

    auto s = std::format("{:<10} id={:04X} val={:8.2f}", name, id, val);
    std::puts(s.c_str());

Why: `std::format` keeps advanced formatting readable without manual buffer sizing or brittle format-string argument ordering.

Trade-offs: Formatter support has been uneven across toolchains, so portability and binary size may matter.

When not to do this: Do not adopt `std::format` blindly in portability-sensitive or hot formatting paths without checking support and cost.

References: [cppreference - std::format](https://en.cppreference.com/w/cpp/utility/format)
```

Input:

```text
Modernize this API to C++23. The code passes raw pointers around, but the caller docs do not say whether the callee owns them:

void set_buffer(Buffer* buffer);
```

Expected output:

```text
Assessment: The production risk is ambiguous ownership and lifetime; changing this blindly could introduce leaks, double deletes, or dangling access.

Recommended change: Do not replace the raw pointer with a smart pointer yet. First document whether `set_buffer` observes, borrows, or takes ownership, then modernize to separate observer and owner APIs if needed.

Code:

    class Consumer {
    public:
        void set_buffer(Buffer* buffer) noexcept { buffer_ = buffer; }
    private:
        Buffer* buffer_ = nullptr; // observer only after ownership is clarified
    };

Why: Ownership clarity is the first modernization step; once that contract is explicit, you can choose references, `std::span`, or smart pointers without guessing.

Trade-offs: This keeps the legacy pointer storage for now and requires follow-up documentation work before a full API cleanup.

When not to do this: Do not use the observer-style rewrite if the function actually transfers ownership or accepts null as a meaningful state.

References: [cppreference - std::unique_ptr](https://en.cppreference.com/w/cpp/memory/unique_ptr)
```

Input:

```text
This function is part of a public shared-library API used by third parties. Can I modernize it to std::string_view and std::expected?

extern "C++" bool parse_name(const char* input, Result* out);
```

Expected output:

```text
Assessment: The production risk is ABI breakage for downstream binaries if you change the exported signature to standard-library types.

Recommended change: Keep the boundary stable and modernize internally first; only add a new C++23-facing overload if you can version the API and coordinate rebuilds.

Why: `std::string_view` and `std::expected` can improve clarity, but exported shared-library interfaces need compatibility planning, not blanket modernization.

Trade-offs: Preserving the old signature keeps compatibility but means you carry an adapter layer and may not expose the nicest C++23 API immediately.

No code change at boundary:

    bool parse_name(const char* input, Result* out) {
        auto view = std::string_view(input ? input : "");
        return parse_name_impl(view, *out);
    }

References: [cppreference - std::string_view](https://en.cppreference.com/w/cpp/string/basic_string_view)
```

Input:

```text
We compile with exceptions disabled. Modernize this bool + out-parameter API:

bool load_config(Config& out);
```

Expected output:

```text
Assessment: The production risk is recommending an exception-oriented or poorly supported result type in a build that explicitly disables exceptions.

Recommended change: Keep the non-throwing policy explicit and return a small status object or enum-based result instead of jumping straight to `std::expected`.

Code:

    enum class load_config_status {
        ok,
        file_missing,
        parse_error,
    };

    struct load_config_result {
        load_config_status status;
        Config value;
    };

    load_config_result load_config();

Why: This removes the out-parameter while staying compatible with exception-disabled builds and mixed toolchains.

Trade-offs: A custom result type is more verbose than `std::expected` and needs local conventions for checking success.

When not to do this: Do not prefer the custom result wrapper if the codebase already standardizes on `std::expected` and your library support is confirmed.

References: [cppreference - std::expected](https://en.cppreference.com/w/cpp/utility/expected)
```

Input:

```text
This loop runs in a packet-processing hot path. Should I rewrite it with ranges/views?

for (size_t i = 0; i < n; ++i) {
    if ((values[i] & mask) != 0) {
        out.push_back(values[i] * scale);
    }
}
```

Expected output:

```text
Assessment: The production risk is adding iterator-adapter overhead or harder-to-profile control flow in a hot path where branch cost and allocation behavior matter.

Recommended change: Keep the conventional loop shape, but reserve output capacity and make the intent explicit instead of forcing a ranges pipeline.

Code:

    out.reserve(n);
    for (size_t i = 0; i < n; ++i) {
        if ((values[i] & mask) != 0) {
            out.push_back(values[i] * scale);
        }
    }

Why: The indexed loop is direct, easy to profile, and less likely to hide temporary objects or view-lifetime issues in allocator-sensitive code.

Trade-offs: You keep a manual loop and give up some compositional style compared with `views::filter` and `views::transform`.

When not to do this: Do not keep the hand-written loop by default if profiling shows the code is not hot and a range pipeline materially improves readability without regression.

References: [cppreference - ranges](https://en.cppreference.com/w/cpp/ranges)
```

Input:

```text
This queue is used by multiple threads. Suggest a C++23 modernization:

while (!done_) {
    if (ready_) {
        consume(item_);
        ready_ = false;
    }
}
```

Expected output:

```text
Assessment: The production risk is changing thread-safety or wake-up assumptions in code that already has concurrency-sensitive shared state.

Recommended change: Replace the busy-wait loop with an explicit `std::condition_variable`-based handoff so synchronization stays correct and visible.

Code:

    std::unique_lock lock(mutex_);
    cv_.wait(lock, [&] { return done_ || ready_; });
    if (done_) return;
    auto item = item_;
    ready_ = false;
    lock.unlock();
    consume(item);

Why: This removes spinning and makes the coordination contract explicit without inventing a racy lock-free rewrite.

Trade-offs: Blocking synchronization is more intrusive than a cosmetic cleanup and requires the producer side to notify the condition variable correctly.

When not to do this: Do not switch to this pattern blindly if the queue already depends on a lock-free design or specific latency behavior that must be preserved.

References: [cppreference - std::condition_variable](https://en.cppreference.com/w/cpp/thread/condition_variable)
```

Input:

```text
This function is called from C code in a plugin boundary. Should I change it to std::span<std::byte> and std::expected<void, Error>?

extern "C" int parse_packet(const uint8_t* data, size_t len, Packet* out);
```

Expected output:

```text
Assessment: The production risk is breaking the C ABI and foreign-call expectations by exposing C++ library types at a C plugin boundary.

Recommended change: Keep the exported C signature as-is and modernize only inside the implementation with `std::span` and internal C++ result handling.

Why: C interop boundaries should stay plain and stable; safer C++23 types belong behind the adapter layer unless every caller can move with you.

Trade-offs: You keep the older signature and some conversion code, but you avoid ABI churn across plugin or language boundaries.

Internal-only example:

    extern "C" int parse_packet(const uint8_t* data, size_t len, Packet* out) {
        return parse_packet_impl(
            std::span<const std::byte>(reinterpret_cast<const std::byte*>(data), len),
            out);
    }

References: [cppreference - std::span](https://en.cppreference.com/w/cpp/container/span)
```

Input:

```text
Should I rewrite this into a ranges pipeline?

for (const auto& msg : messages) {
    if (!msg.enabled()) continue;
    log_ready(msg.id(), msg.payload());
}
```

Expected output:

```text
Assessment: The production risk is making a simple side-effecting loop harder to debug by hiding control flow inside a pipeline.

Recommended change: Keep the conventional loop; this is already clear production code, and a ranges pipeline is not a free readability upgrade.

Code:

    for (const auto& msg : messages) {
        if (!msg.enabled()) continue;
        log_ready(msg.id(), msg.payload());
    }

Why: For side effects and early-continue logic, the loop is direct and avoids view lifetime questions or extra adaptor noise.

Trade-offs: You give up a more declarative style and some composability if the processing later grows into a reusable pure transformation pipeline.

When not to do this: Do not keep the manual loop if the code evolves into a pure filter/transform pipeline with no side effects and clear lifetime boundaries.

References: [cppreference - std::ranges::filter_view](https://en.cppreference.com/w/cpp/ranges/filter_view)
```

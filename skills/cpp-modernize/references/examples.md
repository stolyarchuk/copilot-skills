# Examples

Input:

```text
Modernize this function that concatenates strings using `sprintf` and raw buffers.

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
Summary: Replace unsafe C string handling with `std::string`/`std::string_view` and standard algorithms.

    #include <string>
    #include <string_view>
    #include <iostream>

    void join(std::span<const std::string_view> parts) {
        std::string out;
        for (auto sv : parts) out += sv;
        std::cout << out << '\n';
    }

Reference: [cppreference - basic_string](https://en.cppreference.com/w/cpp/string/basic_string)
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
Summary: Use iterator- or range-based construction to avoid manual loops.

    #include <vector>
    #include <ranges>

    void copy(const int* arr, size_t n) {
        std::vector<int> v(std::ranges::begin(std::span(arr, n)), std::ranges::end(std::span(arr, n)));
    }

Reference: [cppreference - ranges](https://en.cppreference.com/w/cpp/ranges)
```

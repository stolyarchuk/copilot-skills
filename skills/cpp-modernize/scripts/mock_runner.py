#!/usr/bin/env python3
"""Minimal mock runner for `cpp-modernize` examples.

It applies a small, deterministic transformation to input examples for smoke tests.
"""

import sys


def modernize_text(s: str) -> str:
    s = s.strip()
    if "sprintf" in s or "strcat" in s:
        return (
            "Summary: Replace unsafe C string handling with `std::string`/`std::string_view` and standard algorithms.\n\n"
            "    #include <string>\n    #include <string_view>\n    #include <iostream>\n\n    void join(std::span<const std::string_view> parts) {\n        std::string out;\n        for (auto sv : parts) out += sv;\n        std::cout << out << '\\n';\n    }\n\n"
            "Reference: [cppreference - basic_string](https://en.cppreference.com/w/cpp/string/basic_string)"
        )
    if "for (size_t i = 0; i < n; ++i) v.push_back(arr[i]);" in s:
        return (
            "Summary: Use iterator- or range-based construction to avoid manual loops.\n\n"
            "    #include <vector>\n    #include <ranges>\n\n    void copy(const int* arr, size_t n) {\n        std::vector<int> v(std::ranges::begin(std::span(arr, n)), std::ranges::end(std::span(arr, n)));\n    }\n\n"
            "Reference: [cppreference - ranges](https://en.cppreference.com/w/cpp/ranges)"
        )
    return s


if __name__ == "__main__":
    data = sys.stdin.read()
    out = modernize_text(data)
    sys.stdout.write(out)

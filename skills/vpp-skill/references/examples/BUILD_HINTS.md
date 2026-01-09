Minimal build hints for the example files

- Standalone (for quick local compile & smoke run):

  g++ -std=c++23 -O2 -fPIC -c plugin.cpp -o plugin.o
  gcc -std=c23 -O2 -c vpp_node.c -o vpp_node.o
  g++ -shared -o libvpp_plugin.so plugin.o vpp_node.o

- Notes when integrating into VPP build:
  - Add the C node `vpp_node.c` to the plugin's VPP module sources and ensure
    it links against the C++ implementation or static object compiled with
    `-std=c++23`.
  - Do not allow C++ exceptions to cross the C boundary; catch them inside
    C++ and translate to error codes (as shown in `plugin.cpp`).
  - Prefer allocating the C `vpp_plugin_ctx_t` with `malloc`/`free` or expose
    clear ownership rules; keep ABI simple.

- Example linker flags you might need:
  - `-Wl,--no-undefined` to catch missing symbols at link time
  - Link against DPDK/VPP libs when building inside the VPP tree

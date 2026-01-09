#pragma once

/* C++23 header for plugin implementation. Keep C++ internals out of the
 * public C API. The C API (`c_api.h`) is the single, stable bridge used by
 * VPP-facing C files.
 */

#include "../c_api.h"
#include <cstddef>

namespace vpp_plugin {

class PluginImpl {
 public:
  explicit PluginImpl(const char* config_path) noexcept;
  ~PluginImpl();

  /* Process a batch of buffers passed by VPP. Return number processed or
   * a negative error code on failure. */
  int process_batch(void** buffers, size_t n) noexcept;

 private:
  size_t processed_count_;
};

}  // namespace vpp_plugin

/* C++23 implementation for the example plugin. This file implements the
 * minimal C API declared in `../c_api.h` and delegates to
 * `vpp_plugin::PluginImpl`.
 *
 * Important: No exceptions escape across the C API boundary. All C API
 * functions are `extern "C"` with C-compatible signatures.
 */

#include "plugin.hpp"
#include <new>
#include <cstdio>
#include <cstdlib>

using namespace vpp_plugin;

/* Concrete definition of the opaque C handle from `c_api.h`. */
struct vpp_plugin_ctx_s {
  PluginImpl* impl;
};

/* PluginImpl implementation */
PluginImpl::PluginImpl(const char* config_path) noexcept : processed_count_(0) {
  /* In real code parse config_path, initialize DPDK/VPP resources, etc. */
  (void)config_path;
}

PluginImpl::~PluginImpl() { /* release resources if any */ }

int PluginImpl::process_batch(void** buffers, size_t n) noexcept {
  if (!buffers || n == 0) return 0;
  /* Minimal illustrative processing: touch each buffer pointer and count */
  for (size_t i = 0; i < n; ++i) {
    (void)buffers[i]; /* In real code cast to vlib_buffer_t* and operate */
    ++processed_count_;
  }
  return (int)n;
}

/* C API implementations - keep them noexcept and C ABI compatible */
extern "C" {

vpp_plugin_ctx_t* vpp_plugin_init(const char* config_path, int* out_rc) {
  if (out_rc) *out_rc = VPP_PLUGIN_ERR;
  vpp_plugin_ctx_t* ctx = nullptr;
  try {
    ctx = (vpp_plugin_ctx_t*)std::malloc(sizeof(vpp_plugin_ctx_t));
    if (!ctx) return nullptr;
    ctx->impl = new PluginImpl(config_path);
  } catch (...) {
    if (ctx) std::free(ctx);
    if (out_rc) *out_rc = VPP_PLUGIN_ERR;
    return nullptr;
  }
  if (out_rc) *out_rc = VPP_PLUGIN_OK;
  return ctx;
}

void vpp_plugin_shutdown(vpp_plugin_ctx_t* ctx) {
  if (!ctx) return;
  delete ctx->impl;
  std::free(ctx);
}

int vpp_plugin_process_batch(vpp_plugin_ctx_t* ctx, void** buffers, size_t n) {
  if (!ctx || !ctx->impl) return VPP_PLUGIN_ERR;
  try {
    return ctx->impl->process_batch(buffers, n);
  } catch (...) {
    /* Never let exceptions escape; translate to error */
    return VPP_PLUGIN_ERR;
  }
}

}  // extern "C"

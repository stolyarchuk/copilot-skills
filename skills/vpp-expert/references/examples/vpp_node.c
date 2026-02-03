/* Minimal VPP node example (C23).
 *
 * This file is illustrative. In a real VPP plugin you would use the
 * VPP-provided types and registration macros (vlib_node_registration_t,
 * VLIB_REGISTER_NODE, etc.). The important part shown here is how a
 * VPP C node can call into the C API exported by a C++ implementation.
 */

#include <stddef.h>
#include <stdio.h>
#include "../c_api.h" /* Include the generated minimal C API */

/* Minimal stand-in for a VPP frame. Real VPP frames carry vlib_buffer_t *
 * and an integer vector of buffer indices. For clarity we use void* pointers
 * in this example which would represent `vlib_buffer_t*` in real code.
 */
typedef struct {
  void** buffers;
  size_t n_vectors;
} vlib_frame_t;

/* Global plugin context, managed during plugin init/shutdown */
static vpp_plugin_ctx_t* g_plugin_ctx = NULL;

/* Called at plugin initialization (for example from a proper VPP init function)
 */
int vpp_plugin_node_init(const char* config_path) {
  int rc = VPP_PLUGIN_ERR;
  g_plugin_ctx = vpp_plugin_init(config_path, &rc);
  if (!g_plugin_ctx) return rc; /* propagate error code */
  return VPP_PLUGIN_OK;
}

/* Main node processing function - called for each frame */
size_t vpp_plugin_node_process(vlib_frame_t* frame) {
  if (g_plugin_ctx == NULL || frame == NULL || frame->n_vectors == 0) return 0;

  /* Delegate to plugin fast-path API */
  int processed =
      vpp_plugin_process_batch(g_plugin_ctx, frame->buffers, frame->n_vectors);
  if (processed < 0) {
    /* handle error: in real code translate to VPP error counters */
    return 0;
  }
  return (size_t)processed;
}

/* Called at plugin shutdown */
void vpp_plugin_node_shutdown(void) {
  if (g_plugin_ctx) {
    vpp_plugin_shutdown(g_plugin_ctx);
    g_plugin_ctx = NULL;
  }
}

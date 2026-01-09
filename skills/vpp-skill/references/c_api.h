/* Minimal draft c_api.h exposing C++ plugin to VPP C files. */
#ifndef VPP_PLUGIN_C_API_H
#define VPP_PLUGIN_C_API_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stddef.h>

/* Opaque context handle returned by C++ plugin initializer */
typedef struct vpp_plugin_ctx_s vpp_plugin_ctx_t;

/* Return codes */
enum vpp_plugin_rc_e {
  VPP_PLUGIN_OK = 0,
  VPP_PLUGIN_ERR = -1,
};

/* Initialize plugin; returns context or NULL on failure */
vpp_plugin_ctx_t* vpp_plugin_init(const char* config_path, int* out_rc);

/* Cleanup and free plugin context */
void vpp_plugin_shutdown(vpp_plugin_ctx_t* ctx);

/* Example fast-path packet processing entry called from VPP node */
int vpp_plugin_process_batch(vpp_plugin_ctx_t* ctx, void** buffers, size_t n);

#ifdef __cplusplus
}
#endif

#endif /* VPP_PLUGIN_C_API_H */

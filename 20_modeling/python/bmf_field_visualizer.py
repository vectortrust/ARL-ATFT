# bmf_field_visualizer.py
import numpy as np
import pyopencl as cl
from mayavi import mlab
import time

# ---- OpenCL Setup ----
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
kernel_code = """
kernel void overlay_sum(global const float *x, global float *out, const float t)
{
    int gid = get_global_id(0);
    float xval = x[gid];
    float fn1 = sin(2.0f * 3.14159f * xval - 0.5f * t);
    float fn2 = 0.5f * cos(3.0f * 3.14159f * xval + 0.3f * t);
    out[gid] = fn1 + fn2;
}
"""
prg = cl.Program(ctx, kernel_code).build()

# ---- Data Setup ----
x = np.linspace(0, 2, 500).astype(np.float32)
y = np.zeros_like(x)
z = np.zeros_like(x)
out = np.empty_like(x)

d_x = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=x)
d_out = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, out.nbytes)

# ---- Mayavi Setup ----
fig = mlab.figure(bgcolor=(0, 0, 0), size=(1000, 600))
plot = mlab.plot3d(x, y, z, out, tube_radius=0.01, colormap='Spectral')

# ---- Animate ----
try:
    t0 = time.time()
    while True:
        t = np.float32(time.time() - t0)
        prg.overlay_sum(queue, x.shape, None, d_x, d_out, t)
        cl.enqueue_copy(queue, out, d_out)
        plot.mlab_source.set(z=out, scalars=out)
        mlab.process_ui_events()
        time.sleep(0.03)  # ~33 FPS
except KeyboardInterrupt:
    pass

mlab.close()

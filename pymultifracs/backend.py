JAX_AVAILABLE = False

try:
    import jax
    import jax.numpy as jnp
    from jax import jit, vmap
    
    print(f'JAX:{jax.__version__} found, using JAX routines')
    
    JAX_AVAILABLE = True
    
    try:
        import xarray_jax
    except ImportError:
        print('xarray_jax not found, some features may be broken')
    
except ImportError:
    jax = None
    import numpy as jnp
    
    def jit(f, *a, **k): return f
    def vmap(f, *a, **k): return f
    
    print('JAX not found, using numpy routines')

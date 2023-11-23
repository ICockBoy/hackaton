from .start import router as start
from .register import router as register


routers = [start, register]
__all__ = ['routers']

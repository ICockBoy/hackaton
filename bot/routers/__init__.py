from .start import router as start
from .register import router as register
from .admin import router as admin
from .add_house import router as add_house


routers = [start, admin, register, add_house]
__all__ = ['routers']

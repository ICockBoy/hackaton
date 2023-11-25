from .start import router as start
from .register import router as register
from .admin import router as admin
from .add_house import router as add_house
from .reports import router as reports


routers = [start, admin, register, add_house, reports]
__all__ = ['routers']

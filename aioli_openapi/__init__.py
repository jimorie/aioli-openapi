from aioli import Package

from .controller import HttpController
from .service import OpenApiService
from .config import ConfigSchema

export = Package(
    controllers=[HttpController],
    services=[OpenApiService],
    config=ConfigSchema,
    auto_meta=True
)

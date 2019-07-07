from aioli import Package
from .controller import HttpController
from .service import OpenApiService
from .config import ConfigSchema

export = Package(
    name="aioli_openapi",
    version="0.1.0",
    description="Generate OpenAPI Schemas using Aioli Controllers",
    controllers=[HttpController],
    services=[OpenApiService],
    config=ConfigSchema
)

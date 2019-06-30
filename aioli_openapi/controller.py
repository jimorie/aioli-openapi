from aioli.utils import jsonify

from aioli.controller import (
    BaseHttpController,
    ParamsSchema,
    Method,
    route,
    takes,
)

from .service import OpenApiService
from .schema import PathSchema


class HttpController(BaseHttpController):
    def __init__(self, pkg):
        super(HttpController, self).__init__(pkg)
        self.openapi = OpenApiService(pkg)

    @route("/", Method.GET, "List of OAS-compatible Schemas")
    @takes(query=ParamsSchema)
    async def packages_get(self, query):
        data = await self.openapi.get_schemas(**query)
        return jsonify(data, status=200)

    @route("/{package_name}", Method.GET, "Single OAS-compatible Schema for a Package")
    @takes(path=PathSchema)
    async def package_get(self, package_name):
        data = await self.openapi.get_schema(package_name)
        return jsonify(data, status=200)

from aioli.utils import jsonify

from aioli.controller import (
    BaseHttpController,
    Method,
    schemas,
    route,
    takes,
    returns,
)

from .service import OpenApiService
from .schema import OpenApiPath


class HttpController(BaseHttpController):
    def __init__(self, pkg):
        super(HttpController, self).__init__(pkg)
        self.openapi = OpenApiService(pkg)

    @route("/", Method.GET, "List of OAS3 Schemas")
    @takes(query=schemas.HttpParams)
    @returns(status=200, many=True)
    async def packages_get(self, query):
        return await self.openapi.get_schemas(**query)

    @route("/{package_name}", Method.GET, "Single OAS3 Schema for a Package")
    @takes(path=OpenApiPath)
    @returns(status=200)
    async def package_get(self, package_name):
        return await self.openapi.get_schema(package_name)

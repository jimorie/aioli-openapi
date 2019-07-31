import warnings

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from aioli.service import BaseService
from aioli.controller import BaseHttpController
from aioli.exceptions import NoMatchFound


class OpenApiService(BaseService):
    _specs = {}

    def oas_schema(self, pkg):
        spec = APISpec(
            title=pkg.meta["name"].capitalize(),
            version=pkg.meta["version"],
            openapi_version=self.config["oas_version"],
            plugins=[MarshmallowPlugin()],
        )

        for ctrl in pkg.controllers:
            if not isinstance(ctrl, BaseHttpController):
                continue

            routes = {}

            for func, handler in ctrl.handlers:
                if not handler.status:
                    warnings.warn(f"No @returns for {func}, cannot generate OAS3 schema for this handler")
                    break

                abspath = handler.path_full
                method = handler.method.lower()

                if abspath not in routes:
                    routes[abspath] = {}

                if method not in routes[abspath]:
                    routes[abspath][method] = dict(
                        responses={},
                        parameters=[]
                    )

                route = routes[abspath][method]
                responses = route["responses"]
                parameters = route["parameters"]

                for location, schema_cls in handler.schemas:
                    if location == "response":
                        if not schema_cls:
                            content = {}
                        else:
                            content = {"application/json": {"schema": schema_cls}}

                        responses[handler.status] = dict(
                            description=None,
                            content=content
                        )
                    elif location in ["path", "query", "header"]:
                        if not schema_cls:
                            continue

                        parameters.append({
                            "in": location,
                            "schema": schema_cls
                        })

                spec.path(handler.path_full, operations=routes[abspath])

        return spec.to_dict()

    async def on_startup(self):
        for pkg in self.app.registry.imported:
            if not pkg.config["path"]:
                continue

            self._specs[pkg.meta["name"]] = self.oas_schema(pkg)

    async def get_schemas(self, **query):
        return self._specs

    async def get_schema(self, name):
        if name not in self._specs:
            raise NoMatchFound

        return self._specs[name]

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from aioli.service import BaseService
from aioli.controller import BaseHttpController
from aioli.exceptions import NoMatchFound

from ._apispec import OpenApi


class OpenApiService(BaseService):
    schemas = {}

    async def on_startup(self):
        for pkg, module in self.app.registry.imported.values():
            if not pkg.config["path"]:
                continue

            spec = APISpec(
                title=pkg.name.capitalize(),
                version=pkg.version,
                openapi_version="3.0.2",
                plugins=[MarshmallowPlugin()],
            )

            # spec = OpenApi(pkg)
            # print(self.spec.components.schema('User', schema=pkg))

            for ctrl in pkg.controllers:
                if not isinstance(ctrl, BaseHttpController):
                    continue

                for handler, route_stack in ctrl.stacks:
                    response = route_stack.schemas.response

                    from aioli.controller import schema

                    if issubclass(response, schema.Schema):
                        print(response)
                        spec.components.schema("Hej", schema=response())

            # self.schemas[pkg.name] = spec.schema

    async def get_schemas(self, **query):
        return self.schemas.values()

    async def get_schema(self, name):
        """schemas = dict(self.schemas)
        if name not in schemas:
            raise NoMatchFound

        spec = APISpec(
            title="Swagger Petstore",
            version="1.0.0",
            openapi_version="3.0.2",
            plugins=[MarshmallowPlugin()],
        )

        # spec.components.schema('User', schema=schemas[name])

        # print(spec.to_dict()["definitions"])
        print(schemas[name])"""

        # return schemas[name]
        # print(self.schemas)
        return {}

from enum import Enum


class ParamType(Enum):
    query = "query"
    path = "path"
    header = "header"
    body = "body"


class OpenApi:
    _routes = None

    def __init__(self, pkg):
        self.swagger = "2.0"
        self.info = dict(
            title=pkg.name.capitalize(),
            version=pkg.version,
            description=pkg.description.capitalize(),
        )

        self._routes = {}

    def _get_field_type(self, field):
        return field.__class__.__name__.lower()

    def _get_params(self, schema, param_type):
        if not schema:
            return

        for field_name, field in schema.declared_fields.items():
            required = True if param_type == ParamType.path else field.required

            yield {
                'name': field_name,
                'in': param_type.value,
                'description': '',
                'required': required,
                'type': self._get_field_type(field)
            }

    def get_path_params(self, schema):
        return list(self._get_params(schema, ParamType.path))

    def get_query_params(self, schema):
        return list(self._get_params(schema, ParamType.query))

    def get_body_params(self, schema):
        return list(self._get_params(schema, ParamType.body))

    def get_response(self, schema):
        if not schema:
            return {"description": "Undefined response"}

        fields = {}
        # load_only = schema.Meta.load_only
        load_only = []

        for field_name, field in schema._declared_fields.items():
            if field_name in load_only:
                continue

            if hasattr(field, 'nested'):
                fields[field_name] = self.get_response(field.nested)
                continue

            fields[field_name] = dict(type=self._get_field_type(field))

        response = {
            'type': 'object',
            'properties': fields
        }

        if hasattr(schema, 'many') and schema.many:
            return {
                'type': 'array',
                **response
            }

        return response

    def consume_stack(self, handler, route_stack):
        schemas = route_stack.schemas
        definition = dict(
            parameters=[]
        )

        if route_stack.path not in self._routes:
            self._routes[route_stack.path] = {}

        if schemas["body"]:
            definition['parameters'] += self.get_query_params(schemas['body'])

        if schemas['query']:
            definition['parameters'] += self.get_query_params(schemas['query'])

        if schemas["path"]:
            definition['parameters'] += self.get_path_params(schemas['path'])

        response = self.get_response(schemas['response'])
        definition['responses'] = {
            '200': dict(
                description="",
                schema=response
            )
        }

        method = route_stack.method.lower()
        self._routes[route_stack.path].update({
            method: {
                'description': route_stack.description,
                'operationId': handler.__name__,
                **definition,
            }
        })

    @property
    def schema(self):
        schema = self.__dict__
        routes = schema.pop('_routes')

        return {
            **schema,
            'paths': routes
        }

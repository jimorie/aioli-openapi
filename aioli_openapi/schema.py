from aioli.controller.schemas import fields, Schema


class OpenApiPath(Schema):
    package_name = fields.String()

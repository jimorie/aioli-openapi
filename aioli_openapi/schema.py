from aioli.controller.schema import fields, Schema


class PathSchema(Schema):
    package_name = fields.String()

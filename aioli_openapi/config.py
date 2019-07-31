from aioli.config import PackageConfigSchema, fields


class ConfigSchema(PackageConfigSchema):
    path = fields.String(missing="/openapi")
    oas_version = fields.String(required=False, missing="3.0.2")

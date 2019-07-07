from aioli.config import PackageConfigSchema, fields


class ConfigSchema(PackageConfigSchema):
    oas_version = fields.String(required=False, missing="3.0.2")

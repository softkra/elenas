from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
class CustomerGeneratorSchema(OpenAPISchemaGenerator):
    def get_operation(self, *args, **kwargs):
        operation = super().get_operation(*args, **kwargs)
        authorization_header = openapi.Parameter(
            name="Authorization",
            description="Authorization Header",
            required=True,
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            default="Token <token>"
        )
        operation.parameters.append(authorization_header)
        return operation
    
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema
"""OpenAPI schema helpers.

Everything here only affects the generated schema (Swagger / Redoc /
openapi.yaml). Request handling is untouched.
"""

from drf_spectacular.extensions import OpenApiSerializerExtension
from drf_spectacular.openapi import AutoSchema
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated

WRITE_METHODS = {"POST", "PUT", "PATCH"}


class DetailResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class TokenPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class ErrorDetailSerializer(serializers.Serializer):
    """Body of DRF auth / permission / not-found / throttle errors."""

    detail = serializers.CharField()
    code = serializers.CharField(required=False)


class ValidationErrorSerializer(serializers.Serializer):
    """Marker for DRF validation errors; the real shape is set below."""


class ValidationErrorExtension(OpenApiSerializerExtension):
    target_class = ValidationErrorSerializer

    def map_serializer(self, auto_schema, direction):
        message = {"type": "string"}
        return {
            "type": "object",
            "description": (
                "Field name (or `non_field_errors`, `detail`, `error`) "
                "mapped to a message or a list of messages."
            ),
            "additionalProperties": {
                "oneOf": [{"type": "array", "items": message}, message]
            },
        }


class WearlyAutoSchema(AutoSchema):
    """Adds the error responses a view can actually return.

    Codes declared explicitly via ``@extend_schema(responses=...)`` win.
    """

    def _get_response_bodies(self, direction="response"):
        responses = super()._get_response_bodies(direction)
        if direction != "response":
            return responses

        for code, serializer in self._error_responses().items():
            if code not in responses:
                responses[code] = self._get_response_for_code(
                    serializer, code, direction=direction
                )
        return responses

    def _error_responses(self):
        errors = {}
        if self.method in WRITE_METHODS:
            errors["400"] = ValidationErrorSerializer

        permissions = [
            p for p in self.view.get_permissions() if not isinstance(p, AllowAny)
        ]
        if permissions:
            errors["401"] = ErrorDetailSerializer
        if any(not isinstance(p, IsAuthenticated) for p in permissions):
            errors["403"] = ErrorDetailSerializer

        if "{" in self.path:
            errors["404"] = ErrorDetailSerializer
        if getattr(self.view, "throttle_classes", None):
            errors["429"] = ErrorDetailSerializer
        return errors


class SingleObjectAutoSchema(WearlyAutoSchema):
    def _is_list_view(self, serializer=None):
        return False

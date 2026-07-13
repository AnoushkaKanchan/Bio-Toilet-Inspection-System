from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.serializers import (
    SettingsSerializer,
)
from apps.common.services import (
    SettingsService,
)


class SettingsAPIView(
    APIView,
):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

        self._service = SettingsService()

    def get(
        self,
        request,
    ):
        settings = self._service.get_settings()

        serializer = SettingsSerializer(
            settings,
        )

        return Response(
            serializer.data,
        )
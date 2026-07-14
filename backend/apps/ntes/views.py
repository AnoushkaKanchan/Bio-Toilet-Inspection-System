from apps.inspection.models import Inspection
from apps.ntes.serializers import (
    FetchTrainResponseSerializer,
)
from apps.ntes.services import (
    FetchTrainService,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class FetchTrainAPIView(APIView):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

        self._service = (
            FetchTrainService()
        )

    def post(
        self,
        request,
        inspection_id,
    ):
        try:

            result = self._service.fetch(
                inspection_id=inspection_id,
            )

        except Inspection.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Inspection not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = (
            FetchTrainResponseSerializer(
                result,
            )
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
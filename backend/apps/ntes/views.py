from apps.inspection.models import Inspection
from apps.ntes.serializers import (
    FetchTrainRequestSerializer,
    FetchTrainResponseSerializer,
)
from apps.ntes.services import FetchTrainService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ntes.exceptions import NTESError


class FetchTrainAPIView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = FetchTrainService()

    def post(self, request, inspection_id):

        try:
            serializer = FetchTrainRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            result = self._service.fetch(
                inspection_id=inspection_id,
                train_number=serializer.validated_data["train_number"],
            )

        except Inspection.DoesNotExist:
            return Response(
                {"success": False, "message": "Inspection not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except NTESError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        response_serializer = FetchTrainResponseSerializer(result)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
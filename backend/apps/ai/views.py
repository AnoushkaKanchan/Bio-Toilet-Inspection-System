from apps.ai.exceptions import AIContractError
from apps.ai.serializers import (
    AIAcknowledgementSerializer,
    AIResultRequestSerializer,
)
from apps.ai.services import AIResultService
from apps.inspection.models import Inspection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AIResultAPIView(APIView):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )
        self._service = AIResultService()

    def post(
        self,
        request,
    ):
        serializer = AIResultRequestSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        try:
            acknowledgement = self._service.process(
                inspection_id=serializer.validated_data[
                    "inspection_id"
                ],
                payload=serializer.validated_data[
                    "payload"
                ],
            )

        except AIContractError as exc:
            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Inspection.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Inspection not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        response = AIAcknowledgementSerializer(
            acknowledgement,
        )

        return Response(
            response.data,
            status=status.HTTP_200_OK,
        )
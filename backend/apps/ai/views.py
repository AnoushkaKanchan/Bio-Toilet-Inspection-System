from apps.ai.exceptions import AIContractError, AIPersistenceError, DuplicateAIResultError
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
        #temp
        from django.db import connection
        print("DB:", connection.settings_dict['NAME'], connection.settings_dict['HOST'], connection.settings_dict['PORT'])

        serializer = AIResultRequestSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )
        # temp
        print(serializer.validated_data)

        try:
            acknowledgement = self._service.process(
                payload=serializer.validated_data,
            )

        except AIContractError as exc:
            print("AIContractError:", repr(exc))
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except DuplicateAIResultError as exc:
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_409_CONFLICT,
            )

        except Inspection.DoesNotExist:
            return Response(
                {"success": False, "message": "Inspection not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except AIPersistenceError as exc:
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )
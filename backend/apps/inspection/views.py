from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inspection.models import Inspection
from apps.inspection.serializers import (
    InspectionDetailsItemSerializer,
    InspectionListItemSerializer,
)
from apps.inspection.services import (
    InspectionDetailsService,
    InspectionListService,
)


class InspectionDetailsAPIView(APIView):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._service = InspectionDetailsService()

    def get(
        self,
        request,
        inspection_id,
    ):
        try:
            details = self._service.get_details(
                inspection_id=inspection_id,
            )
        except Inspection.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Inspection not found.",
                },
                status=404,
            )

        serializer = InspectionDetailsItemSerializer(
            details,
        )

        return Response(
            serializer.data,
        )


class InspectionPagination(
    PageNumberPagination,
):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class InspectionListAPIView(
    APIView,
):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._service = InspectionListService()

    def get(
        self,
        request,
    ):
        status = request.query_params.get(
            "status",
        )

        search = request.query_params.get(
            "search",
        )

        try:
            inspections = self._service.list(
                status=status,
                search=search,
            )

        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=400,
            )

        paginator = InspectionPagination()

        page = paginator.paginate_queryset(
            inspections,
            request,
            view=self,
        )

        serializer = InspectionListItemSerializer(
            page,
            many=True,
        )

        return paginator.get_paginated_response(
            serializer.data,
        )

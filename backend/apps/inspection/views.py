from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inspection.serializers import (
    InspectionListItemSerializer,
)
from apps.inspection.services import (
    InspectionListService,
)


class InspectionPagination(
    PageNumberPagination,
):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class InspectionListAPIView(APIView):

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

        try:
            inspections = self._service.list(
                status=status,
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

from io import BytesIO

from django.http import FileResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView, Response

from apps.reports.serializers import (
    CommonDefectSerializer,
    DashboardSummarySerializer,
)
from apps.reports.services import (
    CommonDefectsService,
    DashboardService,
    ExportService,
)


class DashboardView(APIView):

    def get(self, request):
        service = DashboardService()

        serializer = DashboardSummarySerializer(
            service.get_dashboard_summary(),
        )

        return JsonResponse(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CommonDefectsView(APIView):

    def get(self, request):
        service = CommonDefectsService()

        serializer = CommonDefectSerializer(
            service.get_common_defects(),
            many=True,
        )

        return JsonResponse(
            serializer.data,
            safe=False,
            status=status.HTTP_200_OK,
        )


class ExportView(APIView):

    def get(self, request):
        report_type = request.GET.get(
            "type",
            "daily",
        )

        try:
            pdf = ExportService().export(
                report_type=report_type,
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return FileResponse(
            BytesIO(pdf),
            as_attachment=True,
            filename=f"{report_type}_report.pdf",
            content_type="application/pdf",
        )

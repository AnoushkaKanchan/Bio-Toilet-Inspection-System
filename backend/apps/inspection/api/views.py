from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inspection.services.dashboard import DashboardService


class DashboardSummaryView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = DashboardService()

    def get(self, request):
        return Response(
            self._service.get_summary(),
        )
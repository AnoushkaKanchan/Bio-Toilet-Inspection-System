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


class LivePitLineView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = DashboardService()

    def get(self, request):
        return Response(
            self._service.get_live_pitlines(),
        )


class OperationsStatusView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = DashboardService()

    def get(self, request):
        return Response(
            self._service.get_operations_status(),
        )


class RecentActivityView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = DashboardService()

    def get(self, request):
        return Response(
            self._service.get_recent_activity(),
        )


class TrainMappingView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = DashboardService()

    def get(
        self,
        request,
        inspection_id,
    ):
        return Response(
            self._service.get_train_mapping(
                inspection_id=inspection_id,
            )
        )

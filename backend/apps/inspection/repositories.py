from apps.inspection.models import Inspection


class InspectionRepository:
    def get(
        self,
        *,
        inspection_id,
    ) -> Inspection:
        return Inspection.objects.get(
            id=inspection_id,
        )

    def save(
        self,
        *,
        inspection: Inspection,
    ) -> Inspection:
        inspection.save()

        return inspection

from dataclasses import asdict
from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from apps.reports.repositories import ReportsRepository


class ExportService:
    VALID_TYPES = {
        "daily",
        "weekly",
        "monthly",
    }

    def __init__(
        self,
        *,
        repository: ReportsRepository | None = None,
    ) -> None:
        self._repository = repository or ReportsRepository()

    def export(
        self,
        *,
        report_type: str,
    ) -> bytes:
        if report_type not in self.VALID_TYPES:
            raise ValueError(f"Unsupported report type: {report_type}.")

        if report_type == "daily":
            summary = self._repository.get_today_summary()
        elif report_type == "weekly":
            summary = self._repository.get_weekly_summary()
        else:
            summary = self._repository.get_monthly_summary()

        buffer = BytesIO()

        document = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        story = [
            Paragraph(
                f"<b>{report_type.title()} Report</b>",
                styles["Heading1"],
            )
        ]

        for key, value in asdict(summary).items():
            story.append(
                Paragraph(
                    f"{key}: {value}",
                    styles["BodyText"],
                )
            )

        document.build(story)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf

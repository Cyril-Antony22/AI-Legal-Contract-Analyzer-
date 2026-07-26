"""
Module 8 - Export Report
--------------------------
Turns the analysis results (summary, clauses, risks, dates) into a
downloadable file in PDF, CSV, JSON, or TXT format.
"""

import csv
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def format_value(value):
    """Convert any Python object into readable text."""

    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            lines.append(f"{k}: {format_value(v)}")
        return "\n".join(lines)

    elif isinstance(value, list):
        items = []
        for item in value:
            items.append(format_value(item))
        return "\n".join(items)

    else:
        return str(value)


def _flatten_for_rows(analysis):
    """Turn the nested analysis dict into flat (section, content) rows."""
    rows = []

    rows.append(("Summary", format_value(analysis.get("summary", ""))))

    clauses = analysis.get("clauses", {})
    if isinstance(clauses, dict):
        for k, v in clauses.items():
            rows.append((f"Clause - {k}", format_value(v)))
    else:
        rows.append(("Clauses", format_value(clauses)))

    risks = analysis.get("risks", {})
    if isinstance(risks, dict):
        for k, v in risks.items():
            rows.append((f"Risk - {k}", format_value(v)))
    else:
        rows.append(("Risks", format_value(risks)))

    dates = analysis.get("dates_parties", {})
    if isinstance(dates, dict):
        for k, v in dates.items():
            rows.append((f"Info - {k}", format_value(v)))
    else:
        rows.append(("Dates & Parties", format_value(dates)))

    return rows


def export_json(analysis, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    return output_path


def export_txt(analysis, output_path):
    rows = _flatten_for_rows(analysis)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("LEGAL CONTRACT ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")

        for label, content in rows:
            f.write(f"{label}\n")
            f.write("-" * len(label) + "\n")
            f.write(content)
            f.write("\n\n")

    return output_path


def export_csv(analysis, output_path):
    rows = _flatten_for_rows(analysis)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Section", "Content"])

        for row in rows:
            writer.writerow(row)

    return output_path


def export_pdf(analysis, output_path):
    rows = _flatten_for_rows(analysis)

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    story = [
        Paragraph("Legal Contract Analysis Report", styles["Title"]),
        Spacer(1, 20),
    ]

    for label, content in rows:
        story.append(Paragraph(f"<b>{label}</b>", styles["Heading2"]))
        story.append(
            Paragraph(content.replace("\n", "<br/>"), styles["BodyText"])
        )
        story.append(Spacer(1, 12))

    doc.build(story)

    return output_path


def generate_report(analysis, report_folder, filename_base, file_format):
    os.makedirs(report_folder, exist_ok=True)

    output_path = os.path.join(
        report_folder,
        f"{filename_base}.{file_format}"
    )

    if file_format == "pdf":
        return export_pdf(analysis, output_path)

    elif file_format == "csv":
        return export_csv(analysis, output_path)

    elif file_format == "json":
        return export_json(analysis, output_path)

    elif file_format == "txt":
        return export_txt(analysis, output_path)

    else:
        raise ValueError(f"Unsupported format: {file_format}")
import json
from datetime import datetime
from src.analyzer import Issue
from src.metrics import ModuleMetrics, summary

def to_markdown(issues: list, metrics: list, checklist_score: dict = None) -> str:
    md = ["# Code Review Report", ""]
    md.append(f"**Дата:** {datetime.utcnow().isoformat()}")
    md.append("")

    s = summary(metrics)
    md.append("## Метрики")
    for k, v in s.items():
        md.append(f"- **{k}**: {v}")
    md.append("")

    if checklist_score:
        md.append("## Чек-лист")
        md.append(f"- Пройдено: {checklist_score['done']} / {checklist_score['total']}")
        md.append(f"- Оценка: {checklist_score['score']}%")
        md.append("")

    md.append("## Проблемы")
    by_severity = {}
    for i in issues:
        by_severity.setdefault(i.severity, []).append(i)

    for sev in ["critical", "major", "minor"]:
        items = by_severity.get(sev, [])
        if not items:
            continue
        md.append(f"### {sev.upper()} ({len(items)})")
        for i in items[:50]:
            md.append(f"- `{i.file}:{i.line}` **{i.rule_id}** {i.message}")
        md.append("")

    return "\n".join(md)

def to_json(issues: list, metrics: list, path="review.json"):
    data = {
        "generated_at": datetime.utcnow().isoformat(),
        "summary": summary(metrics),
        "issues": [i.__dict__ for i in issues],
        "metrics": [m.__dict__ for m in metrics],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data

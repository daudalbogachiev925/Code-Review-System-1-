from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict

@dataclass
class ModuleMetrics:
    path: str
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    procedures: int = 0
    functions: int = 0
    exports: int = 0
    max_complexity: int = 0
    avg_complexity: float = 0.0
    todo_count: int = 0

def parse_module(path: str) -> ModuleMetrics:
    content = Path(path).read_text(encoding="utf-8", errors="ignore")
    lines = content.split("\n")
    m = ModuleMetrics(path=path, total_lines=len(lines))

    for line in lines:
        stripped = line.strip()
        if not stripped:
            m.blank_lines += 1
        elif stripped.startswith("//"):
            m.comment_lines += 1
        else:
            m.code_lines += 1
            if "TODO" in stripped or "FIXME" in stripped:
                m.todo_count += 1

    m.procedures = content.count("Процедура ")
    m.functions = content.count("Функция ")
    m.exports = content.count("Экспорт")

    complexity = 1
    max_c = 1
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("Если ", "Пока ", "Для ")):
            complexity += 1
            max_c = max(max_c, complexity)
        if stripped.startswith(("КонецЕсли", "КонецЦикла")):
            complexity = max(1, complexity - 1)

    m.max_complexity = max_c
    m.avg_complexity = round(max_c / max(m.procedures + m.functions, 1), 2)
    return m

def analyze_project(root: str) -> List[ModuleMetrics]:
    results = []
    for p in Path(root).rglob("*.bsl"):
        results.append(parse_module(str(p)))
    for p in Path(root).rglob("*.os"):
        results.append(parse_module(str(p)))
    return results

def summary(metrics: List[ModuleMetrics]) -> Dict:
    if not metrics:
        return {}
    total_code = sum(m.code_lines for m in metrics)
    total_comments = sum(m.comment_lines for m in metrics)
    return {
        "modules": len(metrics),
        "total_lines": sum(m.total_lines for m in metrics),
        "code_lines": total_code,
        "comment_lines": total_comments,
        "comment_ratio": round(total_comments / max(total_code, 1) * 100, 1),
        "procedures": sum(m.procedures for m in metrics),
        "functions": sum(m.functions for m in metrics),
        "exports": sum(m.exports for m in metrics),
        "avg_module_size": round(total_code / len(metrics), 1),
        "max_complexity": max((m.max_complexity for m in metrics), default=0),
        "todo_count": sum(m.todo_count for m in metrics),
    }

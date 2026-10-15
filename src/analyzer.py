import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

@dataclass
class Issue:
    file: str
    line: int
    code: str
    severity: str
    message: str
    rule_id: str

@dataclass
class Module:
    path: str
    content: str
    lines: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.lines = self.content.split("\n")

RULES = [
    {
        "id": "BSL001",
        "pattern": r"^\s*[^/\s].*//\s*TODO",
        "severity": "minor",
        "message": "TODO в коде без задачи",
    },
    {
        "id": "BSL002",
        "pattern": r"Сообщить\s*\(",
        "severity": "major",
        "message": "Сообщить() запрещён, используйте ОбщегоНазначения.СообщитьПользователю",
    },
    {
        "id": "BSL003",
        "pattern": r"Предупреждение\s*\(",
        "severity": "major",
        "message": "Предупреждение() запрещено",
    },
    {
        "id": "BSL004",
        "pattern": r"Ждать\s+\d",
        "severity": "major",
        "message": "Магическое число в Ждать",
    },
    {
        "id": "BSL005",
        "pattern": r"Выполнить\s*\(",
        "severity": "critical",
        "message": "Выполнить() — небезопасно",
    },
    {
        "id": "BSL006",
        "pattern": r"НайтиПоНаименованию\s*\(",
        "severity": "major",
        "message": "НайтиПоНаименованию — используйте запрос",
    },
    {
        "id": "BSL007",
        "pattern": r"Ссылка\s*=\s*Справочники\.\w+\.НайтиПоНаименованию",
        "severity": "major",
        "message": "Поиск ссылки по наименованию в цикле",
    },
    {
        "id": "BSL008",
        "pattern": r"&\s*НаКлиенте\s*\n\s*Процедура.*\n(?:(?!КонецПроцедуры).)*&\s*НаСервере",
        "severity": "major",
        "message": "Смешивание директив компиляции",
    },
    {
        "id": "BSL009",
        "pattern": r"\bПароль\s*=\s*[\"']",
        "severity": "critical",
        "message": "Hardcoded пароль",
    },
    {
        "id": "BSL010",
        "pattern": r"\.Найти\s*\(\s*\d+\s*\)",
        "severity": "minor",
        "message": "Магическое число в .Найти()",
    },
]

def analyze_module(path: str) -> List[Issue]:
    content = Path(path).read_text(encoding="utf-8", errors="ignore")
    issues = []
    for i, line in enumerate(content.split("\n"), 1):
        for rule in RULES:
            if re.search(rule["pattern"], line, re.MULTILINE):
                issues.append(Issue(
                    file=path, line=i, code=line.strip()[:100],
                    severity=rule["severity"], message=rule["message"],
                    rule_id=rule["id"]))
    if len(content.split("\n")) > 2000:
        issues.append(Issue(file=path, line=0, code="", severity="major",
                            message="Модуль >2000 строк — разбейте на несколько",
                            rule_id="BSL100"))
    return issues

def analyze_directory(root: str) -> List[Issue]:
    issues = []
    for p in Path(root).rglob("*.bsl"):
        issues.extend(analyze_module(str(p)))
    for p in Path(root).rglob("*.os"):
        issues.extend(analyze_module(str(p)))
    return issues

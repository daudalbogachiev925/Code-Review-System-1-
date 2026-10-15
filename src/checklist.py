CHECKLIST = {
    "functional": [
        "Задача из трекера указана в описании PR",
        "Все критерии приёмки выполнены",
        "Обработаны краевые случаи (пустые, null, отрицательные)",
        "Проверено на тестовой базе",
    ],
    "code": [
        "Код соответствует стандартам 1С",
        "Нет магических чисел",
        "Нет закомментированного кода",
        "Нет TODO без задачи",
        "Нет Отладка.Остановить()",
        "Нет Сообщить() и Предупреждение()",
    ],
    "performance": [
        "Запросы оптимизированы (нет в цикле)",
        "Используются индексы",
        "Нет соединений в цикле",
        "Проверен план запроса",
    ],
    "security": [
        "Нет hardcoded паролей и токенов",
        "Права доступа проверены",
        "Нет Выполнить() и Вычислить() с пользовательскими данными",
        "Проверены RLS-ограничения",
    ],
    "tests": [
        "Юнит-тесты добавлены",
        "Vanessa-сценарии обновлены",
        "Тесты проходят локально",
    ],
    "docs": [
        "README обновлён",
        "CHANGELOG обновлён",
        "Изменения в архитектуре задокументированы",
    ],
}

def render_checklist() -> str:
    lines = ["# Code Review Checklist"]
    for section, items in CHECKLIST.items():
        lines.append(f"\n## {section.capitalize()}")
        for item in items:
            lines.append(f"- [ ] {item}")
    return "\n".join(lines)

def score_checklist(checked: dict) -> dict:
    total = sum(len(items) for items in CHECKLIST.values())
    done = sum(1 for s, items in CHECKLIST.items()
               for it in items if checked.get(f"{s}:{it}", False))
    return {
        "total": total,
        "done": done,
        "score": round(done / total * 100, 1) if total else 0,
    }

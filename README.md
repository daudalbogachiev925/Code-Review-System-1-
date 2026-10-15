# Code-Review-System-1-
 автоматизация code review: статический анализ, метрики, шаблоны, чек-листы, боты для Pull Request.
# 1C Code Review System

Автоматизация code review для 1С-проектов.

## Возможности
- 10+ правил статического анализа BSL/OS
- Метрики модуля: LOC, complexity, comment ratio, TODO
- Чек-лист ревью (6 категорий, 30+ пунктов)
- GitHub-бот для комментариев в PR
- REST API для интеграции

## Запуск
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
pytest -v
```

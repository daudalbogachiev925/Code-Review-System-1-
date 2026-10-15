from src.analyzer import analyze_module
from pathlib import Path
import tempfile

def test_detect_sogobshit():
    with tempfile.NamedTemporaryFile(suffix=".bsl", delete=False, mode="w",
                                     encoding="utf-8") as f:
        f.write("Процедура Тест()\n  Сообщить(\"test\");\nКонецПроцедуры\n")
        path = f.name
    issues = analyze_module(path)
    assert any(i.rule_id == "BSL002" for i in issues)

def test_detect_magic_number():
    with tempfile.NamedTemporaryFile(suffix=".bsl", delete=False, mode="w",
                                     encoding="utf-8") as f:
        f.write("Ждать 5;\n")
        path = f.name
    issues = analyze_module(path)
    assert any(i.rule_id == "BSL004" for i in issues)

def test_detect_hardcoded_password():
    with tempfile.NamedTemporaryFile(suffix=".bsl", delete=False, mode="w",
                                     encoding="utf-8") as f:
        f.write('Пароль = "secret123";\n')
        path = f.name
    issues = analyze_module(path)
    assert any(i.rule_id == "BSL009" for i in issues)

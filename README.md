# Загрузка russian-pii-66k

Установите зависимость и загрузите датасет:

```bash
venv/bin/pip install -r requirements.txt
venv/bin/python russian_pii_66k.py
```

Файл `data/russian_pii_66k.jsonl` содержит исходные поля `source_text`,
`privacy_mask`, `language` и `locale`. Каждый элемент `privacy_mask` содержит
символьные границы `start` и `end`, метку `label` и текст `value`. Загрузчик
проверяет, что `source_text[start:end] == value` для каждой сущности.

Путь можно изменить через `--output`. Для воспроизводимого запуска укажите
коммит датасета через `--revision`.

Источник: https://huggingface.co/datasets/wolframko/russian-pii-66k

Карточка датасета не содержит описания происхождения данных и лицензии.
Перед дальнейшим использованием проверьте условия публикации и качество разметки
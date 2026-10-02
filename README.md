# Загрузка russian-pii-66k

Установите зависимость и загрузите датасет:

```bash
venv/bin/pip install -r requirements.txt
venv/bin/python scripts/downloaders/russian_pii_66k.py
```

Файл `data/russian_pii_66k.jsonl` содержит исходные поля `source_text`,
`privacy_mask`, `language` и `locale`. Каждый элемент `privacy_mask` содержит
символьные границы `start` и `end`, метку `label` и текст `value`. Загрузчик
проверяет, что `source_text[start:end] == value` для каждой сущности.

Путь можно изменить через `--output`. Для воспроизводимого запуска укажите
коммит датасета через `--revision`.

Источник: https://huggingface.co/datasets/wolframko/russian-pii-66k

Карточка датасета не содержит описания происхождения данных и лицензии.
Перед дальнейшим использованием проверьте условия публикации и качество разметки.

## Тест русской модели spaCy

Для воспроизведения теста установите модель и запустите
`notebooks/testing/spacy_ru_russian_pii_66k.ipynb` из установленного ядра `venv`:

```bash
venv/bin/python -m spacy download ru_core_news_sm
venv/bin/python scripts/downloaders/russian_pii_66k.py \
  --revision d458b5a2e299d2e16adbd3b3921487f652b06a96
venv/bin/python -m ipykernel install --user --name spacy-up --display-name "Python (spacy-up)"
```

Состав выборки (1000 записей, seed 42) и SHA-256 исходного JSONL записаны в
`notebooks/testing/russian_pii_66k_test_manifest.json`. Ноутбук проверяет файл
перед оценкой. Он сравнивает только совместимые группы имён и локаций с метками
`PER` и `LOC` модели; остальные типы перечисляет отдельно.

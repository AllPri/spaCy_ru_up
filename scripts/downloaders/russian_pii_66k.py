"""Загружает и проверяет русскоязычный набор размеченных персональных данных."""

import argparse
from collections import Counter
from collections.abc import Mapping
from pathlib import Path

from datasets import load_dataset


DATASET_ID = "wolframko/russian-pii-66k"
REQUIRED_COLUMNS = {"source_text", "privacy_mask", "language", "locale"}


def validate_row(row: object, index: int) -> Counter[str]:
    """Проверяет, что границы каждой сущности совпадают с исходным текстом."""
    if not isinstance(row, Mapping):
        raise ValueError(f"Запись {index}: ожидается словарь с полями датасета")
    source_text = row["source_text"]
    entities = row["privacy_mask"]
    if not isinstance(source_text, str) or not isinstance(entities, list):
        raise ValueError(f"Запись {index}: неверный тип текста или списка сущностей")

    counts = Counter()
    for entity in entities:
        if not isinstance(entity, Mapping):
            raise ValueError(f"Запись {index}: сущность должна быть словарём")
        start, end = entity.get("start"), entity.get("end")
        label, value = entity.get("label"), entity.get("value")
        if (
            type(start) is not int
            or type(end) is not int
            or not 0 <= start < end <= len(source_text)
            or not isinstance(label, str)
            or not label
            or not isinstance(value, str)
            or source_text[start:end] != value
        ):
            raise ValueError(f"Запись {index}: неверная сущность {entity!r}")
        counts[label] += 1
    return counts


def load_russian_pii_66k(revision: str | None = None):
    """Возвращает обучающую выборку Hugging Face в исходной схеме."""
    dataset = load_dataset(DATASET_ID, split="train", revision=revision)
    missing = REQUIRED_COLUMNS - set(dataset.column_names)
    if missing:
        raise ValueError(f"В датасете отсутствуют поля: {', '.join(sorted(missing))}")
    return dataset


def main() -> None:
    """Сохраняет проверенную выборку в JSONL и выводит число сущностей по меткам."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/russian_pii_66k.jsonl"),
        help="Путь к итоговому JSONL",
    )
    parser.add_argument("--revision", help="Коммит или тег датасета на Hugging Face")
    args = parser.parse_args()

    dataset = load_russian_pii_66k(args.revision)
    counts = Counter()
    for index, row in enumerate(dataset):
        counts.update(validate_row(row, index))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_json(str(args.output), orient="records", lines=True, force_ascii=False)
    print(f"Сохранено записей: {len(dataset)} → {args.output}")
    print("Сущности: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))


if __name__ == "__main__":
    main()

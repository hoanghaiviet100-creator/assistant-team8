
import argparse
import csv
import re
import sys
from pathlib import Path


def normalize(text: str) -> str:
    """Normalize text before exact-match comparison."""
    text = text.casefold().strip()
    return re.sub(r"\s+", " ", text)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"question", "expected", "category"}

        if not required.issubset(reader.fieldnames or []):
            raise ValueError(
                f"{path} must contain columns: "
                "question, expected, category"
            )

        rows = list(reader)

    if not rows:
        raise ValueError(f"{path} contains no test cases")

    valid_categories = {"normal", "edge", "out-of-scope"}

    for index, row in enumerate(rows, start=2):
        if row["category"] not in valid_categories:
            raise ValueError(
                f"Invalid category at CSV line {index}: "
                f"{row['category']}"
            )

        if not row["question"].strip() or not row["expected"].strip():
            raise ValueError(
                f"Empty question or expected value at CSV line {index}"
            )

    return rows


def evaluate(
    cases: list[dict[str, str]],
    predictions: list[dict[str, str]],
) -> None:
    if len(cases) != len(predictions):
        raise ValueError(
            f"Expected {len(cases)} predictions, "
            f"but received {len(predictions)}"
        )

    results = []

    for case, prediction in zip(cases, predictions):
        expected = normalize(case["expected"])
        actual = normalize(prediction["answer"])
        results.append({
            "category": case["category"],
            "correct": expected == actual,
        })

    correct = sum(result["correct"] for result in results)
    total = len(results)

    print(f"Overall accuracy: {correct}/{total} ({correct / total:.2%})")
    print("\nAccuracy by category:")

    for category in ("normal", "edge", "out-of-scope"):
        group = [
            result for result in results
            if result["category"] == category
        ]

        if not group:
            print(f"  {category}: no cases")
            continue

        group_correct = sum(result["correct"] for result in group)
        print(
            f"  {category}: {group_correct}/{len(group)} "
            f"({group_correct / len(group):.2%})"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate sensitive-information redaction cases."
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("eval/cases.csv"),
        help="Path to the test cases CSV",
    )
    parser.add_argument(
        "--predictions",
        type=Path,
        default=Path("eval/predictions.csv"),
        help="CSV containing model answers in an 'answer' column",
    )
    args = parser.parse_args()

    try:
        cases = load_csv(args.cases)
        predictions = load_csv(args.predictions)

        if "answer" not in predictions[0]:
            raise ValueError(
                f"{args.predictions} must contain an 'answer' column"
            )

        evaluate(cases, predictions)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

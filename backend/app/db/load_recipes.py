import argparse
import csv
import math
from pathlib import Path
from typing import Mapping

from app.db.database import init_db
from app.db.session import SessionLocal
from app.models.recipe import Recipe

DEFAULT_CSV_PATH = Path(__file__).resolve().parents[3] / "dataset" / "cleaned_recipes.csv"
REQUIRED_COLUMNS = {
    "recipe_id",
    "nama_masakan",
    "kategori",
    "jumlah_porsi",
    "basis_porsi",
    "kalori_kkal",
    "protein_g",
    "karbohidrat_g",
    "lemak_g",
    "bahan_bahan",
    "cara_memasak",
    "url",
}


def _cell(row: Mapping[str, str | None], column: str) -> str:
    return (row.get(column) or "").strip()


def _optional_text(row: Mapping[str, str | None], column: str) -> str | None:
    return _cell(row, column) or None


def _optional_float(row: Mapping[str, str | None], column: str, line_number: int) -> float | None:
    raw_value = _cell(row, column)
    if raw_value.lower() in {"", "nan", "none", "null"}:
        return None

    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ValueError(
            f"CSV baris {line_number}: kolom '{column}' harus berupa angka."
        ) from exc

    if not math.isfinite(value):
        raise ValueError(f"CSV baris {line_number}: kolom '{column}' harus berupa angka finite.")
    return value


def parse_recipe_row(row: Mapping[str, str | None], line_number: int) -> Recipe:
    recipe_id = _cell(row, "recipe_id")
    nama_masakan = _cell(row, "nama_masakan")
    if not recipe_id:
        raise ValueError(f"CSV baris {line_number}: 'recipe_id' wajib diisi.")
    if not nama_masakan:
        raise ValueError(f"CSV baris {line_number}: 'nama_masakan' wajib diisi.")

    raw_servings = _cell(row, "jumlah_porsi")
    try:
        jumlah_porsi = int(raw_servings) if raw_servings else 1
    except ValueError as exc:
        raise ValueError(
            f"CSV baris {line_number}: kolom 'jumlah_porsi' harus berupa bilangan bulat."
        ) from exc
    if jumlah_porsi <= 0:
        raise ValueError(f"CSV baris {line_number}: 'jumlah_porsi' harus lebih besar dari 0.")

    return Recipe(
        recipe_id=recipe_id,
        nama_masakan=nama_masakan,
        kategori=_optional_text(row, "kategori"),
        jumlah_porsi=jumlah_porsi,
        basis_porsi=_cell(row, "basis_porsi") or "1 porsi",
        kalori_kkal=_optional_float(row, "kalori_kkal", line_number),
        protein_g=_optional_float(row, "protein_g", line_number),
        karbohidrat_g=_optional_float(row, "karbohidrat_g", line_number),
        lemak_g=_optional_float(row, "lemak_g", line_number),
        bahan_bahan=_optional_text(row, "bahan_bahan"),
        cara_memasak=_optional_text(row, "cara_memasak"),
        url=_optional_text(row, "url"),
    )


def read_recipes_csv(csv_path: Path) -> list[Recipe]:
    recipes: list[Recipe] = []
    seen_recipe_ids: set[str] = set()

    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise ValueError(f"CSV tidak memiliki header: {csv_path}")

        headers = [header.strip() for header in reader.fieldnames]
        if len(headers) != len(set(headers)):
            raise ValueError("CSV memiliki nama kolom yang duplikat.")

        missing_columns = REQUIRED_COLUMNS.difference(headers)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Kolom berikut tidak ditemukan pada CSV: {missing}")
        reader.fieldnames = headers

        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"CSV baris {line_number}: jumlah nilai tidak sesuai dengan header.")

            recipe = parse_recipe_row(row, line_number)
            if recipe.recipe_id in seen_recipe_ids:
                raise ValueError(
                    f"CSV baris {line_number}: recipe_id '{recipe.recipe_id}' muncul lebih dari sekali."
                )
            seen_recipe_ids.add(recipe.recipe_id)
            recipes.append(recipe)

    if not recipes:
        raise ValueError(f"CSV tidak berisi data resep: {csv_path}")
    return recipes


def load_recipes(csv_path: Path) -> int:
    recipes = read_recipes_csv(csv_path)
    init_db()

    with SessionLocal.begin() as session:
        for recipe in recipes:
            session.merge(recipe)

    return len(recipes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Muat resep dari CSV ke tabel PostgreSQL recipes.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV_PATH,
        help="Lokasi CSV resep (default: dataset/cleaned_recipes.csv di root project).",
    )
    args = parser.parse_args()

    if not args.csv.is_file():
        parser.error(f"File CSV tidak ditemukan: {args.csv}")

    count = load_recipes(args.csv)
    print(f"Berhasil memuat atau memperbarui {count} resep dari {args.csv}.")


if __name__ == "__main__":
    main()

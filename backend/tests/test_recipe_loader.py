import pytest

from app.db.load_recipes import parse_recipe_row


def _recipe_row() -> dict[str, str]:
    return {
        "recipe_id": "RCP_TEST",
        "nama_masakan": "Contoh Resep",
        "kategori": "Makanan Utama",
        "jumlah_porsi": "2",
        "basis_porsi": "1 porsi",
        "kalori_kkal": "250.5",
        "protein_g": "20",
        "karbohidrat_g": "30",
        "lemak_g": "8",
        "bahan_bahan": "Ayam, nasi",
        "cara_memasak": "Masak hingga matang.",
        "url": "https://example.test/resep",
    }


def test_parse_recipe_row_maps_csv_fields_and_empty_nutrition():
    row = _recipe_row()
    row["kalori_kkal"] = ""

    recipe = parse_recipe_row(row, line_number=2)

    assert recipe.recipe_id == "RCP_TEST"
    assert recipe.nama_masakan == "Contoh Resep"
    assert recipe.jumlah_porsi == 2
    assert recipe.kalori_kkal is None
    assert recipe.protein_g == 20.0
    assert recipe.bahan_bahan == "Ayam, nasi"


def test_parse_recipe_row_reports_invalid_numeric_value_with_line_number():
    row = _recipe_row()
    row["protein_g"] = "bukan-angka"

    with pytest.raises(ValueError, match="CSV baris 7.*protein_g"):
        parse_recipe_row(row, line_number=7)

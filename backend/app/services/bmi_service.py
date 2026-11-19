from app.core.config import settings

# Catatan Standar Klasifikasi BMI:
# Default sistem menggunakan standar Kementerian Kesehatan RI ("kemenkes").
# Untuk mengganti ke standar WHO global ("who"), ubah BMI_STANDARD=who di file .env
# atau ubah nilai default BMI_STANDARD di app/core/config.py.
# Format setiap aturan: (batas_atas, inklusif, label_kategori)
BMI_STANDARDS: dict[str, list[tuple[float, bool, str]]] = {
    "kemenkes": [
        (17.0, False, "Sangat Kurus"),
        (18.5, False, "Kurus"),
        (25.0, True, "Normal"),
        (27.0, True, "Gemuk"),
        (float("inf"), True, "Obesitas"),
    ],
    "who": [
        (18.5, False, "Underweight"),
        (25.0, False, "Normal"),
        (30.0, False, "Overweight"),
        (float("inf"), True, "Obese"),
    ],
}


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Menghitung Body Mass Index (BMI / IMT) dari berat badan (kg) dan tinggi badan (cm)."""
    if weight_kg <= 0:
        raise ValueError("weight_kg harus lebih besar dari 0.")
    if height_cm <= 0:
        raise ValueError("height_cm harus lebih besar dari 0.")

    height_m = height_cm / 100.0
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi: float, standard: str | None = None) -> str:
    """Menentukan kategori BMI berdasarkan standar yang dipilih (default: kemenkes)."""
    if bmi <= 0:
        raise ValueError("Nilai BMI harus lebih besar dari 0.")

    active_standard = (standard or settings.BMI_STANDARD).lower()
    rules = BMI_STANDARDS.get(active_standard)
    if rules is None:
        supported = ", ".join(sorted(BMI_STANDARDS.keys()))
        raise ValueError(f"Standar BMI '{active_standard}' tidak dikenal. Pilihan: {supported}.")

    for upper_bound, inclusive, label in rules:
        if (bmi <= upper_bound) if inclusive else (bmi < upper_bound):
            return label

    return rules[-1][2]


# DietMate AI — Backend FastAPI

Backend layanan nutrisi dan validasi meal plan untuk **DietMate AI**.

## Fitur yang Sudah Tersedia

- `GET /health` — Health check status server.
- `POST /nutrition/calculate` — Menghitung BMI, BMR (Mifflin-St Jeor), TDEE (PAL), target kalori harian, serta target makronutrien dalam gram.
- `POST /nutrition/validate` — Memvalidasi meal plan dengan menghitung ulang nutrisi langsung dari database PostgreSQL (`recipes`), memeriksa hard constraint (`recipe_id`, porsi, dan alergen melalui pencocokan teks pada `bahan_bahan`), serta soft constraint (toleransi deviasi nutrisi `±10%` dan batas pengulangan resep maksimal `2` kali).
- `POST /mealplan/generate` — Endpoint stub/placeholder yang menyusun meal plan bebas alergen dari tabel `recipes`, memvalidasinya, dan menyimpannya ke tabel `meal_plans` PostgreSQL.
- `GET /mealplan/{id}` — Mengambil hasil meal plan tersimpan dari tabel `meal_plans`.

---

## Catatan Konfigurasi Standar Gizi

1. **Standar BMI (Default: Kemenkes RI)**
   - Nilai `BMI_STANDARD` pada `.env` secara default disetel ke `kemenkes` (`Sangat Kurus < 17.0`, `Kurus 17.0–18.4`, `Normal 18.5–25.0`, `Gemuk 25.1–27.0`, `Obesitas > 27.0`).
   - Jika ingin beralih ke standar WHO global (`Underweight`, `Normal`, `Overweight`, `Obese`), cukup ubah `BMI_STANDARD=who` di `.env` (atau ubah definisi ambang batas pada `BMI_STANDARDS` di `app/services/bmi_service.py`).
2. **Distribusi Makronutrien**
   - Default rasio energi: **50% Karbohidrat**, **20% Protein**, **30% Lemak** (berada dalam rentang Pedoman Gizi Seimbang: Karbohidrat 45–65%, Protein 10–20%, Lemak 20–35%, total wajib 100%).
3. **Batas Pengulangan Resep**
   - Default `MAX_RECIPE_REPEATS=2` (maksimal 2 kali per bulan / periode rencana makan).

---

## Setup & Menjalankan Server

1. Pastikan berada di folder `backend/` dan virtual environment `.venv` sudah terpasang dependensi:
   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
2. Salin `.env.example` menjadi `.env` (jika belum ada) dan sesuaikan kredensial PostgreSQL (`dietmate_db`):
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/dietmate_db
   ```
   Pastikan service PostgreSQL berjalan. Tabel database dibuat otomatis saat FastAPI pertama kali dijalankan (`init_db()`), atau dapat dibuat dengan perintah loader resep di bawah.

### Memuat data resep

Loader membaca `dataset/cleaned_recipes.csv` dari root project, membuat tabel yang belum ada, lalu memasukkan atau memperbarui resep berdasarkan `recipe_id`. Jalankan dari folder `backend/`:

```powershell
.\.venv\Scripts\python.exe -m app.db.load_recipes
```

Untuk memakai CSV di lokasi lain, berikan path secara eksplisit:

```powershell
.\.venv\Scripts\python.exe -m app.db.load_recipes --csv "D:\path\ke\cleaned_recipes.csv"
```
3. Jalankan server FastAPI:
   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```
4. Akses dokumentasi interaktif:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

---

## Menjalankan Pengujian (Pytest)

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```


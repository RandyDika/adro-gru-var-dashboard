# Dashboard ADRO GRU + VaR

Dashboard Flask ini menyajikan keluaran notebook Colab. Dashboard tidak melatih ulang model.

## Menyiapkan hasil Colab

Unduh `adro_gru_complete_outputs.zip` dari sesi Colab yang menjalankan notebook, ekstrak, lalu letakkan folder hasilnya di direktori yang sama dengan `app.py`. Aplikasi menerima nama folder `outputs` maupun `adro_gru_complete_outputs`. Struktur minimal:

```text
outputs/
  run_metadata.json
  data/adro_usdidr.csv
  predictions/A_T5_U512_RMSPROP_B64_predictions.csv
  predictions/one_step_forecast_summary.csv
  var/adro_var_summary.csv
```

Data dan ramalan pada notebook saat ini berakhir pada 30 April 2026. Jangan gunakan ramalan itu sebagai ramalan terkini tanpa memperbarui dan menjalankan kembali notebook.

## Menjalankan aplikasi

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask run
```

Buka alamat lokal yang ditampilkan Flask. Jika berkas keluaran belum ada, dashboard menampilkan ringkasan angka notebook serta penanda bahwa grafik dan data yang membutuhkan berkas belum dimuat.

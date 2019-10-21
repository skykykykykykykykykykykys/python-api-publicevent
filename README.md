# Python API for Public Event

## Description

API yang melayani permintaan klien mengenai fasilitas ITB yang sedang digunakan pada tanggal tersebut.

### Informasi yang akan diberikan :
- Tanggal
- Nama Peminjam Fasilitas beserta Fasilitas yang digunakan
- Detail Penggunaan


## How to Use

### GET "./jadwal"

Sistem akan memberikan keluaran berupa kegiatan apa saja yang diselenggarakan di kawasan ITB pada bulan dimana permintaan GET tersebut dijalankan
```
$curl -X GET http://localhost:8080/jadwal
```

### GET "./jadwal/{tanggal}"

Sistem akan memberikan keluaran berupa kegiatan apa saja yang diselenggarakan di kawasan ITB pada tanggal query tersebut
```
$curl -X GET http://localhost:8080/jadwal?tanggal=<tgl>
```

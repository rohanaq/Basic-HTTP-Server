Basic HTTP Server
========================
Tugas 2 Pemrograman Jaringan D

Deskripsi:
-------------
1. Menggunakan pustaka socket biasa
2. Buatlah HTTP server yang menangani request dari klien
3. Buatlah satu halaman html dan satu halaman php di sisi server
4. Halaman html dan php inilah yang di-request oleh klien
5. Buatlah direktori dataset yang berisi file-file. Selanjutnya, klien bisa masuk dengan mengkliknya, melihat list file, dan mengunduh file di dalam direktori dataset
6. Klien bisa melihat daftar isi direktori 'dataset' karena tidak ada file index.html di dalamnya
7. Respon yang didukung oleh server adalah 200 OK dan 404 Not Found (bisa ditambahkan yang lain)
8. Server dapat diakses dengan browser client yang umum digunakan, misalnya Firefox dan Chrome
9. Port server yang digunakan server (misalnya port 80) harus disimpan di dalam file terpisah, tidak boleh disimpan dalam source code
10. Klien dapat mengakses file PHP dan menampilkan isi script hasil pengolahan PHP (Hint: bisa menggunakan pemanggilan perintah shell PHP-CLI dari Python)

Penggunaan: 
-------------
```
1. Jalankan file server.py
2. Buka browser lalu akses localhost dengan port 7676
```
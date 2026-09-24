---
name: 9router-image
description: Generate images and diagrams via 9Router /v1/images/generations using models like gemini-3.1-flash-image, nanobanana, gpt-image. Use for rendering flowcharts, architectural diagrams, and illustrations.
---

# 9Router — Image Generation

Endpoint untuk menghasilkan gambar, diagram alir, atau ilustrasi menggunakan 9Router di `http://localhost:20128`.

## Endpoint & Format Request

`POST http://localhost:20128/v1/images/generations`

```json
{
  "model": "ag/gemini-3.1-flash-image",
  "prompt": "Technical flowchart showing audio digital signal processing pipeline...",
  "size": "1024x1024"
}
```

Tambahkan query `?response_format=binary` jika ingin menyimpan langsung ke berkas biner `.png`.

### Contoh cURL:

```bash
curl -X POST "http://localhost:20128/v1/images/generations?response_format=binary" \
  -H "Content-Type: application/json" \
  -d '{"model":"ag/gemini-3.1-flash-image","prompt":"clean scientific diagram of audio FFT spectrum to DMX lighting","size":"1024x1024"}' \
  --output image.png
```

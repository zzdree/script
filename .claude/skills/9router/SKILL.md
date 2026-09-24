---
name: 9router
description: Entry point for 9Router — local/remote AI gateway with OpenAI-compatible REST for chat, image, TTS, embeddings, web search, web fetch. Use when interacting with 9Router at localhost:20128 or VPS.
---

# 9Router — Gateway AI Multi-Provider

Gateway AI lokal/remote yang menyediakan antarmuka REST kompatibel OpenAI dengan auto-fallback lintas provider.

## Setup & Koneksi Lokal

- **Default URL:** `http://localhost:20128`
- **Health Check:** `curl http://localhost:20128/api/health` ➔ `{"ok":true}`
- **Header Auth:** `Authorization: Bearer ${NINEROUTER_KEY}` (opsional jika auth lokal dinonaktifkan).

## Penemuan Model (Model Discovery)

```bash
curl http://localhost:20128/v1/models                  # LLM / Chat
curl http://localhost:20128/v1/models/image            # Image Generation
curl http://localhost:20128/v1/models/embedding        # Embeddings
curl http://localhost:20128/v1/models/stt              # Speech-to-Text
curl http://localhost:20128/v1/models/tts              # Text-to-Speech
```

Gunakan `data[].id` sebagai parameter `model` saat melakukan request API.

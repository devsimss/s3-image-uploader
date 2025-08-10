
# S3 Image Uploader (Presigned PUT)

## Türkçe
Küçük bir dosya yükleme örneği. Sunucu tarafı yalnızca **S3 için imzalı PUT URL** üretir; dosya doğrudan tarayıcıdan S3’e gider. Yerel geliştirme sırasında CORS ve içerik tipi kontrolü yapılır.

### Kurulum
1. Bir S3 bucket oluşturun ve örnekteki CORS ayarını uygulayın.
2. Backend:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # bucket adını ve origin'i girin
   uvicorn server:app --reload
   ```
3. Frontend:
   ```bash
   cd ../frontend
   python -m http.server 5500
   # http://localhost:5500
   ```

### Not
- Örnek amaçlı `public-read` kullanıldı. Üretimde erişimi sınırlamak ve indirmeleri de imzalı URL ile yapmak gerekir.

---

## English
Tiny upload sample. The server issues a **presigned PUT URL** for S3; the browser uploads the file directly to S3. CORS and basic content-type checks are included for local development.

### Setup
1. Create an S3 bucket and apply the CORS config in the example.
2. Backend:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   uvicorn server:app --reload
   ```
3. Frontend:
   ```bash
   cd ../frontend
   python -m http.server 5500
   # http://localhost:5500
   ```

### Note
- `public-read` is used for demonstration. In real deployments, prefer restricted access and signed GETs.

# Negatif Stok Kontrolü

Bu uygulama, **ERPNext v15.78.1** üzerinde **seçili depolarda negatif stoğa izin verilmemesini** sağlar.  
Global **Negatif Stoğa İzin Ver** ayarı açık olsa bile, belirlenen depolarda negatif stok **yasaktır**.

---

## 📌 Özellikler
- **Global kontrol**: `Stock Settings > Stok Doğrulamaları >Negatif Stoğa İzin Ver` kapalıysa → hiçbir depoda negatif stok yapılamaz.  
- **Depo bazlı kısıtlama**: Global ayar açık olsa bile, `Restricted Negative Stock Warehouse` formuna eklenen depolarda negatif stok yasaktır.  
- **Esneklik**: Listede olmayan depolarda negatif stok serbesttir.  

---

## ⚙️ Kurulum

```bash
cd frappe-bench
bench get-app https://github.com/KTA-Endustri-Sistemleri/negative_stock_control.git
bench --site sitename install-app negative_stock_control
bench --site sitename migrate
```

---

## 🚀 Kullanım

1. ERPNext’te **Stok Ayarları (Stock Settings)** ekranına gidin.  
2. **Negatif Stoğa İzin Ver** kutusunu işaretleyin.  
3. Açılan tabloda negatif stoğa izin verilmemesi gereken depoları seçin.  
4. Artık:  
   - Listelenen depolarda negatif stok → **ValidationError** fırlatılır.  
   - Diğer depolarda negatif stok → **izin verilir**.  

---
[![ERPNext App Tests](https://github.com/KTA-Endustri-Sistemleri/negative_stock_control/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/KTA-Endustri-Sistemleri/negative_stock_control/actions/workflows/tests.yml)
## 🧪 Testler 

İki senaryo test edilir:  
1. Negatif stok **restricted depoda** → hata vermeli ✅  
2. Negatif stok **restricted olmayan depoda** → izin verilmeli ✅  

Testleri çalıştırmak için:  

```bash
bench --site sitename run-tests --app negative_stock_control
```

---

## 🔄 Sürekli Entegrasyon

Bu repo için **GitHub Actions** tabanlı otomatik test entegrasyonu vardır.  
Her **push** ve **pull request** sonrası testler çalışır.  

### 📂 Workflow

`.github/workflows/tests.yml` içinde tanımlıdır.  

### ✅ Avantajlar
- Her commit sonrası otomatik test  
- PR merge olmadan testler geçmeli  
- Hataları erkenden yakalar  

---

## 📜 Lisans
MIT

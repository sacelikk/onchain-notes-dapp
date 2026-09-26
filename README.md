# 🔒 On-Chain Secure Note DApp

Solidity akıllı sözleşmeleri, Hardhat yerel geliştirme ağı ve Streamlit arayüzü kullanılarak geliştirilmiş merkeziyetsiz not defteri uygulaması (DApp).

## 🚀 Özellikler

- **Adres Bazlı Veri İzolasyonu:** `SecureNotes.sol` sözleşmesi üzerinde `msg.sender` bazlı eşleme (`mapping(address => Note[])`) ile her kullanıcının notları kendi cüzdanına bağlanır.
- **Yerel Blokzincir Entegrasyonu:** Hardhat yerel düğümü (`http://127.0.0.1:8545`) ve `Web3.py` kütüphanesi üzerinden işlem imzalama ve blok üretimi.
- **İnteraktif Arayüz:** Streamlit tabanlı, cüzdan bakiyesi sorgulama, işlem hash takibi ve zaman damgalı not listeleme desteği.

## 🛠️ Teknoloji Yığını

- **Akıllı Sözleşme:** Solidity `^0.8.20`
- **Geliştirme & Dağıtım:** Hardhat v3 (ESM / Viem)
- **Arayüz:** Streamlit (Python)
- **Web3 Sağlayıcısı:** Web3.py

## 📦 Kurulum ve Çalıştırma

### 1. Bağımlılıkları Yükleyin

Proje dizinine girip JavaScript ve Python paketlerini kurun:

```bash
cd zincir_not_defteri
npm install
pip install streamlit web3 cryptography

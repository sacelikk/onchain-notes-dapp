import streamlit as st
from web3 import Web3
import json
import os
from datetime import datetime

# 1. Blokzincir Bağlantısı
RPC_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# 2. Kontrat Bilgileri
CONTRACT_ADDRESS = Web3.to_checksum_address("0x5fbdb2315678afecb367f032d93f642f64180aa3")

# ABI'yi derlenen artifact dosyasından dinamik olarak oku
artifact_path = os.path.join("artifacts", "contracts", "SecureNotes.sol", "SecureNotes.json")
with open(artifact_path, "r", encoding="utf-8") as f:
    artifact = json.load(f)
CONTRACT_ABI = artifact["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# 3. Streamlit Sayfa Düzeni
st.set_page_config(page_title="Zincir Üstü Not Defteri", page_icon="📝", layout="centered")
st.title("🔒 Zincir Üstü Not Defteri (Web3)")


user_private_key = st.text_input("Cüzdan Özel Anahtarı (Private Key):", type="password")

if user_private_key:
    try:
        account = w3.eth.account.from_key(user_private_key)
        user_address = account.address
        balance = w3.eth.get_balance(user_address)
        
        st.info(f"**Bağlı Cüzdan:** `{user_address}`  \n**Bakiye:** {w3.from_wei(balance, 'ether')} ETH")

        st.divider()

        # Not Ekleme Formu
        st.subheader("➕ Yeni Not Ekle")
        with st.form("note_form", clear_on_submit=True):
            title = st.text_input("Başlık")
            content = st.text_area("İçerik")
            submitted = st.form_submit_button("Zincire Kaydet")

            if submitted:
                if not title or not content:
                    st.warning("Lütfen başlık ve içerik alanlarını doldurun.")
                else:
                    with st.spinner("İşlem blokzincire yazılıyor..."):
                        nonce = w3.eth.get_transaction_count(user_address)
                        tx = contract.functions.addNote(title, content).build_transaction({
                            "chainId": 31337,
                            "gas": 300000,
                            "gasPrice": w3.eth.gas_price,
                            "nonce": nonce,
                            "from": user_address
                        })
                        signed_tx = w3.eth.account.sign_transaction(tx, private_key=user_private_key)
                        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

                        st.success(f"Not bloğa eklendi! Tx Hash: `{tx_hash.hex()}`")

        st.divider()

        # Notları Listeleme
        st.subheader("📋 Kayıtlı Notlarım")
        notes = contract.functions.getMyNotes().call({"from": user_address})

        if not notes:
            st.write("Bu cüzdana ait henüz kayıtlı bir not bulunamadı.")
        else:
            for note in reversed(notes):
                note_id = note[0]
                note_title = note[1]
                note_content = note[2]
                note_time = datetime.fromtimestamp(note[3]).strftime("%Y-%m-%d %H:%M:%S")

                with st.expander(f"📌 {note_title} (#{note_id})"):
                    st.write(note_content)
                    st.caption(f"Kayıt Tarihi: {note_time}")

    except Exception as e:
        st.error(f"Bağlantı veya İşlem Hatası: {e}")
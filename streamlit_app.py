import streamlit as st
from streamlit_qrcode_generator import qrcode_gen
from PIL import Image
from io import BytesIO

st.title("QR Code Generator")

# ユーザーからのURL入力を受け付ける
url = st.text_input("Enter the URL to generate QR code for:")

if url:
    # QRコードを生成
    qr_code_image = qrcode_gen(url)

    # QRコードを表示
    if qr_code_image is not None:
        # ★★★ ここを修正 ★★★
        # use_column_width=True を削除し、width でサイズを直接指定する
        st.image(qr_code_image, caption=f"QR Code for: {url}", width=250)

        # PILイメージをバイトデータに変換
        buf = BytesIO()
        qr_code_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # ダウンロードボタン
        st.download_button(
            label="Download QR Code",
            data=byte_im,
            file_name="qrcode.png",
            mime="image/png"
        )

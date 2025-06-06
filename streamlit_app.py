import streamlit as st
import qrcode
from PIL import Image, ImageDraw  # ← この行を修正
import io

st.set_page_config(layout="wide")
st.title("ロゴ入り＆カラフルQRコードメーカー🎨")

# --- サイドバー（入力部分） ---
st.sidebar.header("QRコードの設定")

# 1. QRコードにしたいテキストやURLを入力
qr_data = st.sidebar.text_input("QRコードにしたいテキストやURLを入力", "https://www.google.com/")

# 2. 色を選択
fill_color = st.sidebar.color_picker('ドットの色', '#000000')
back_color = st.sidebar.color_picker('背景色', '#FFFFFF')

# 3. ロゴ画像をアップロード
logo_image = st.sidebar.file_uploader("中央に配置するロゴ画像を選択（PNG推奨）", type=['png', 'jpg', 'jpeg'])

# --- メイン画面（QRコード表示部分） ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("設定プレビュー")
    if logo_image:
        st.image(logo_image, caption="アップロードされたロゴ", use_column_width=True)
    else:
        st.info("ロゴをアップロードするとここに表示されます。")

with col2:
    st.subheader("生成されたQRコード")
    if not qr_data:
        st.warning("テキストまたはURLを入力してください。")
    else:
        try:
            # --- QRコード生成処理 ---
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H, # H: 高い復元能力
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Pillowを使って色を指定
            qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')

            # --- ロゴを中央に配置する処理 ---
            if logo_image:
                logo = Image.open(logo_image).convert('RGBA')
                
                # ロゴのサイズをQRコードの約1/4にする
                qr_w, qr_h = qr_img.size
                logo_max_size = qr_w // 4
                logo.thumbnail((logo_max_size, logo_max_size))
                
                # ロゴを貼り付ける位置を計算（中央）
                logo_pos = ((qr_w - logo.width) // 2, (qr_h - logo.height) // 2)
                
                # ロゴの背景を透過させるためのマスクを作成
                mask = Image.new('L', logo.size, 0)
                draw = Image.Draw(mask)
                draw.rectangle((0, 0) + logo.size, fill=255)

                qr_img.paste(logo, logo_pos, mask=logo)


            # Streamlitで表示するために画像をバイトデータに変換
            img_bytes = io.BytesIO()
            qr_img.save(img_bytes, format='PNG')
            
            st.image(img_bytes, caption="QRコードが生成されました！", use_column_width=True)

            # ダウンロードボタン
            st.download_button(
                label="画像をダウンロード",
                data=img_bytes.getvalue(),
                file_name="custom_qrcode.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

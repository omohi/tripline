import streamlit as st
import pandas as pd
from icon_data import load_icon_data, get_icon, get_css

# 時間を0埋め形式に変換する関数
def format_time(time_str):
    try:
        return pd.to_datetime(time_str, format='%H:%M').strftime('%H:%M')
    except:
        return time_str

# メインのStreamlitアプリの関数
def main():
    st.set_page_config(layout="wide") 
    st.title("北海道旅行のスケジュール")

    df = pd.read_csv(CSV1_URL)
    df['時間'] = df['時間'].apply(format_time)
    
    # スプレッドシートのURLを設定
    icon_df, icon_classes = load_icon_data(ICON_SHEET_URL)
    
    # CSSを適用
    st.markdown(get_css(icon_classes), unsafe_allow_html=True)
    
    # タイムライン風に表示
    st.write("### スケジュール")
    for index, row in df.iterrows():
        icon, bg_color = get_icon(row['アイコン'], icon_df)  # 備考に応じてアイコンを取得
        st.markdown(f"""
        <div class="schedule-container">
            <div class="time">{row['時間']}</div>
            <div class="icon" style="background-color: {bg_color};">{icon}</div>
            <div class="details">
                <div class="schedule">{row['スケジュール']}</div>
                <div class="remarks">{row['備考']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

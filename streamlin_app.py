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

    # スプレッドシートのURLを設定 (1日目、2日目、3日目)
    df_day1 = load_csv(st.secrets.CSV1_URL)
    df_day2 = load_csv(st.secrets.CSV2_URL)
    df_day3 = load_csv(st.secrets.CSV3_URL)

    # アイコン情報を取得
    icon_df, icon_classes = load_icon_data(st.secrets.ICON_SHEET_URL)
    
    # CSSを適用
    st.markdown(get_css(icon_classes), unsafe_allow_html=True)

    # タブを横いっぱいに広げるためのCSS
    st.markdown("""
        <style>
        div[role="tablist"] > div {
            width: 100%;
            display: flex;
            justify-content: space-evenly;
        }
        button[kind="secondaryTab"] {
            flex-grow: 1;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # タブで日ごとのスケジュールを表示
    tabs = st.tabs(["1日目", "2日目", "3日目"])

    with tabs[0]:
        st.write("### 1日目のスケジュール")
        display_schedule(df_day1, icon_df)
    
    with tabs[1]:
        st.write("### 2日目のスケジュール")
        display_schedule(df_day2, icon_df)
    
    with tabs[2]:
        st.write("### 3日目のスケジュール")
        display_schedule(df_day3, icon_df)

# スケジュール表示用の関数
def display_schedule(df, icon_df):
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

# CSV読み込み用関数
def load_csv(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Failed to load data from {url}: {e}")
        return pd.DataFrame()  # 空のDataFrameを返す

if __name__ == "__main__":
    main()

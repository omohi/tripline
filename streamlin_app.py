import re
import streamlit as st
import pandas as pd
from icon_data import load_icon_data, get_icon, get_css

# 時間を0埋め形式に変換する関数
def format_time(time_str):
    try:
        return pd.to_datetime(time_str, format='%H:%M').strftime('%H:%M')
    except:
        return time_str
								
# URLを検出してリンクまたは画像として変換する関数
def convert_urls_to_links_or_images(text):
    url_pattern = re.compile(r'(https?://\S+)')
    def replace_url(match):
        url = match.group(1)
        if is_image_url(url):
            return f'<img src="{url}" style="max-width: 100%; height: auto;" />'
        else:
            return f'<a href="{url}" target="_blank">{url}</a>'
    return url_pattern.sub(replace_url, text)

# URLが画像かどうかを判断する関数
def is_image_url(url):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    return any(url.lower().endswith(ext) for ext in image_extensions)

# メインのStreamlitアプリの関数
def main():
    st.set_page_config(layout="wide") 
	
    st.markdown(
        """
	<style>
	/* ヘッダーを非表示にする */
	header[data-testid="stHeader"] {
	display: none;
	}
	
	/* ヘッダーのスペースを削除する */
	.stAppViewBlockContainer {
	margin-top: 0 !important;
	padding-top: 0 !important;
	}
	/* スペースを削除するための追加スタイル */
	.element-container,
	.stMarkdown,
	.stMarkdownContainer {
	margin: 0 !important;
	padding: 0 !important;
	}
	</style>
	""",
	unsafe_allow_html=True
    )

    st.title("Hokkaido Trip 0921-0923")

    # スプレッドシートのURLを設定 (1日目、2日目、3日目)
    df_day1 = load_csv(st.secrets.CSV1_URL)
    df_day2 = load_csv(st.secrets.CSV2_URL)
    df_day3 = load_csv(st.secrets.CSV3_URL)

    df_day1['時間'] = df_day1['時間'].apply(format_time)
    df_day2['時間'] = df_day2['時間'].apply(format_time)
    df_day3['時間'] = df_day3['時間'].apply(format_time)

    # アイコン情報を取得
    icon_df, icon_classes = load_icon_data(st.secrets.ICON_SHEET_URL)
    
    # CSSを適用
    st.markdown(get_css(icon_classes), unsafe_allow_html=True)

    # タブで日ごとのスケジュールを表示
    tabs = st.tabs(["Day1", "Day2", "Day3"])

    with tabs[0]:
        display_schedule(df_day1, icon_df)
    
    with tabs[1]:
        display_schedule(df_day2, icon_df)
    
    with tabs[2]:
        display_schedule(df_day3, icon_df)

    # タブを横いっぱいに広げるためのCSS
    st.markdown("""
        <style>
        /* タブ全体を横幅いっぱいに広げる */
        div[role="tablist"] {
            display: flex;
            width: 100%;
        }
        div[role="tablist"] > div {
            flex: 1;
        }
        /* タブのテキストを中央に配置 */
        div[role="tablist"] button {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            text-align: center;
            color: #a6a4c1;
        }
        div[role="tablist"] button[aria-selected="true"] {
            color: #1e1b44;
        }
	div[data-baseweb="tab-highlight"]:not([aria-selected="true"]) {
	    background-color: #1e1b44;
	}
        </style>
    """, unsafe_allow_html=True)

# スケジュール表示用の関数
def display_schedule(df, icon_df):
    for index, row in df.iterrows():
        icon, bg_color = get_icon(row['アイコン'], icon_df)
        remarks = row['備考'] if pd.notna(row['備考']) and row['備考'].strip() != '' else ''
        details = convert_urls_to_links_or_images(row['詳細']) if pd.notna(row['詳細']) else ''
        if pd.notna(row['タイトル']) and row['タイトル'].strip() != '':
            st.markdown(f"""
            <div class="schedule-container">
                <!-- ヘッダー部分は横並び -->
                <div class="schedule-header"  style="display: flex; align-items: center;">
                    <div class="time">{row['時間']}</div>
                    <div class="icon" style="background-color: {bg_color};">{icon}</div>
                    <div class="details">
                        <div class="schedule">{row['スケジュール']}</div>
                        <div class="remarks">{remarks}</div>
                    </div>
                </div>
                <!-- expanderはスケジュールの下に縦並びで表示 -->
                <details class="expander-details" style="display: block; margin-top: 10px;">
                    <summary>{row['タイトル']}</summary>
                    <div class="expander-content">
                        {details}
                    </div>
                </details>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="schedule-container">
                <!-- ヘッダー部分は横並び -->
                <div class="schedule-header"  style="display: flex; align-items: center;">
                    <div class="time">{row['時間']}</div>
                    <div class="icon" style="background-color: {bg_color};">{icon}</div>
                    <div class="details">
                        <div class="schedule">{row['スケジュール']}</div>
                        <div class="remarks">{remarks}</div>
                    </div>
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

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
    st.title("Hokkaido Trip 0921-0923")

    HIDE_ST_STYLE = """
		<style>
		div[data-testid="stToolbar"] {
		visibility: hidden;
		height: 0%;
		position: fixed;
		}
		div[data-testid="stDecoration"] {
		visibility: hidden;
		height: 0%;
		position: fixed;
		}
		#MainMenu {
		visibility: hidden;
		height: 0%;
		}
		header {
		visibility: hidden;
		height: 0%;
		}
		footer {
		visibility: hidden;
		height: 0%;
		}
					.appview-container .main .block-container{
			    padding-top: 1rem;
			    padding-right: 3rem;
			    padding-left: 3rem;
			    padding-bottom: 1rem;
			}  
			.reportview-container {
			    padding-top: 0rem;
			    padding-right: 3rem;
			    padding-left: 3rem;
			    padding-bottom: 0rem;
			}
			header[data-testid="stHeader"] {
			    z-index: -1;
			}
			div[data-testid="stToolbar"] {
			z-index: 100;
			}
			div[data-testid="stDecoration"] {
			z-index: 100;
			}
		</style>
    """
	
    st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

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
            color: #5c588b;
        }
	/* タブの下線の色 */
	div[role="tablist"] button::before {
	    background-color: #1e1b44; /* ここでタブの下線の色を変更できます */
	}
        div[role="tablist"] button[aria-selected="true"] {
            color: #1e1b44;
        }
        </style>
    """, unsafe_allow_html=True)

# スケジュール表示用の関数
def display_schedule(df, icon_df):
    for index, row in df.iterrows():
        icon, bg_color = get_icon(row['アイコン'], icon_df)
        remarks = row['備考'] if pd.notna(row['備考']) and row['備考'].strip() != '' else ''
        st.markdown(f"""
        <div class="schedule-container">
            <div class="time">{row['時間']}</div>
            <div class="icon" style="background-color: {bg_color};">{icon}</div>
            <div class="details">
                <div class="schedule">{row['スケジュール']}</div>
                <div class="remarks">{remarks}</div>
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

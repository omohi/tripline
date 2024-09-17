import pandas as pd

# アイコンと色をスプレッドシートから読み込む
def load_icon_data(sheet_url):
    icon_df = pd.read_csv(sheet_url)
    icon_classes = dict(zip([icon.split(" ")[-1] for icon in icon_df['アイコンクラス']], icon_df['色']))
    return icon_df, icon_classes

# アイコンを取得する関数
def get_icon(remark, icon_df):
    icons = dict(zip(icon_df['アイコン説明'], icon_df['アイコンクラス']))
    colors = dict(zip(icon_df['アイコンクラス'], icon_df['色']))
    icon = icons.get(remark, 'icon-default')  # デフォルトアイコン
    bg_color = colors.get(icon, '#ddd')  # デフォルト背景色
    
    return f'<i class="{icon}"></i>', bg_color

# CSSを生成する関数
def get_css(icon_classes):
    css = """
    <head>
        <!-- Font Awesome CDN -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <style>
    .schedule-container {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        width: 100%;  /* 全幅に対応 */
        border-bottom: 1px solid #ddd;  /* 区切り線の追加 */
        padding-bottom: 10px;  /* 下部に少し余白を追加 */
        justify-content: flex-start;  /* 左寄せに設定 */
    }
    .time {
        font-size: 22px;  /* 少し小さめに変更 */
        color: #474199;
        text-align: left;
        margin-right: 10px;  /* アイコンとの間隔を調整 */
    }
    .icon {
        font-size: 18px;  /* アイコンのサイズを調整 */
        width: 40px;  /* 幅を設定 */
        height: 40px;  /* 高さを設定 */
        margin-right: 10px; /* アイコンとスケジュールの間隔を調整 */
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50% !important;  /* 円形にする */
        position: relative;  /* 円形の背景をアイコンの後ろに配置 */
        color: #fff;  /* アイコンを白にする */
    }
    .icon::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background-color: #ddd;  /* デフォルトの円形背景色 */
        z-index: -1;  /* アイコンの後ろに配置 */
    }
    """
    for icon, color in icon_classes.items():
        icon_before = """
            .{icon}::before {
                background-color: {color};  /* 飛行機アイコンの背景色 */
            }
            """
        css += icon_before
        
    css += """
        .details {
            text-align: left;
        }
        .details .schedule {
            font-size: 18px;  /* スケジュールのフォントサイズを小さめに */
            font-weight: bold;
            color: #333;
        }
        .details .remarks {
            font-size: 14px;  /* 備考のフォントサイズも小さめに */
            color: #555;
        }
        </style>
    """
    return css

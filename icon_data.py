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
    
def get_css(icon_classes):
    css = """
    <head>
        <!-- Font Awesome CDN -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c&display=swap" rel="stylesheet">
    </head>
    <style>
    .schedule-container {
        display: flex;
        flex-direction: column;  /* 垂直方向にアイテムを配置 */
        align-items: flex-start;  /* 左寄せ */
        margin-bottom: 15px;
        width: 100%;  /* 全幅に対応 */
        border-bottom: 1px solid #ddd;  /* 区切り線の追加 */
        padding-bottom: 10px;  /* 下部に少し余白を追加 */
    }
    .schedule-header {
        display: flex;
        align-items: center;
        justify-content: flex-start;  /* 左寄せに設定 */
        width: 100%;  /* ヘッダーも全幅に対応 */
    }
    .time {
        font-size: 22px;  /* 少し小さめに変更 */
        color: #1e1b44;
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
        aspect-ratio: 1/1;  /* アイコンの比率を維持 */
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
        icon_before = f"""
            .{icon}::before {{
                background-color: {color};  /* アイコンの背景色 */
            }}
            """
        css += icon_before

    css += """
        .details {
            text-align: left;
            width: 100%;  /* 詳細部分も全幅に対応 */
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
        .expander-details {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        background-color: #f9f9f9;
        transition: box-shadow 0.3s ease;
        max-width: 100%; /* 横幅の制限 */
        width: 100%; /* 幅をフルにする */
         position: relative; /* 記号の位置調整のため */
        }
        .expander-details:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .expander-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.5s ease;
        background-color: #fff;
        padding: 15px;
        border-radius: 8px;
        max-width: 100%; /* 横幅を一定に保つ */
        }
        .expander-details[open] .expander-content {
        max-height: 500px; /* 必要に応じて調整 */
        }
        summary {
        font-size: 16px;  /* フォントサイズを小さく調整 */
        font-weight: normal;
        color: #666;  /* 色を控えめに変更 */
        cursor: pointer;
        position: relative;
        list-style: none; /* 矢印を削除 */
        padding-left: 0;  /* 左の余白を削除 */
        padding-right: 25px; /* 右の余白を追加 */
        }
        summary::-webkit-details-marker {
        display: none; /* デフォルトのマーカーを非表示 */
        }
        summary::after {
        content: "▶"; /* 右向き三角形 */
        font-size: 18px; /* 記号のサイズ調整 */
        color: #666; /* 記号の色 */
        position: absolute;
        right: 10px; /* 右側に配置 */
        top: 50%;
        transform: translateY(-50%); /* 垂直方向の中央揃え */
        transition: transform 0.3s ease; /* 展開時のアニメーション */
        }
        details[open] summary::after {
        content: "▼"; /* 下向き三角形 */
        transform: translateY(0%) rotate(180deg); /* 記号の向き変更 */
        }
        </style>
    """
    return css

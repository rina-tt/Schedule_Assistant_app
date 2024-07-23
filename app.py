import streamlit as st
import datetime

# スケジュールを保存するリストを初期化
if 'schedule_list' not in st.session_state:
    st.session_state.schedule_list = []

if 'confirmed_schedule' not in st.session_state:
    st.session_state.confirmed_schedule = ""

# ヘッダー
st.title("日程調整アシスト")

# テンプレート入力（現在はデフォルト値として表示）
template = st.text_input("テンプレート", "{month}月{day}日（{weekday}） {start} - {end}")

# 日付選択
selected_date = st.date_input("日付を選択", datetime.date.today())

# 開始時刻選択
start_time = st.time_input("開始時刻を選択", datetime.time(10, 0))

# 終了時刻選択
end_time = st.time_input("終了時刻を選択", datetime.time(12, 0))

# 曜日を取得する関数
def get_weekday_japanese(date):
    weekday_dict = {0: '月', 1: '火', 2: '水', 3: '木', 4: '金', 5: '土', 6: '日'}
    return weekday_dict[date.weekday()]

# テンプレートに基づいてフォーマットする関数
def format_schedule(template, date, start_time, end_time):
    formatted_schedule = template
    formatted_schedule = formatted_schedule.replace("{month}", date.strftime("%m"))
    formatted_schedule = formatted_schedule.replace("{day}", date.strftime("%d"))
    formatted_schedule = formatted_schedule.replace("{weekday}", get_weekday_japanese(date))
    formatted_schedule = formatted_schedule.replace("{start}", start_time.strftime("%H:%M"))
    formatted_schedule = formatted_schedule.replace("{end}", end_time.strftime("%H:%M"))
    return formatted_schedule

# 「追加」ボタンが押された時の処理
if st.button("追加"):
    # 同じ日付がすでに存在するかチェック
    for schedule in st.session_state.schedule_list:
        if schedule["date"] == selected_date:
            st.error("同じ日付がすでに選択されています。スケジュール一覧から直接編集してください。")
            break
    else:
        formatted_schedule = format_schedule(template, selected_date, start_time, end_time)
        st.session_state.schedule_list.append({
            "date": selected_date,
            "start_time": start_time,
            "end_time": end_time,
            "formatted_schedule": formatted_schedule
        })
        st.session_state.schedule_list.sort(key=lambda x: (x['date'], x['start_time']))

# スケジュールリストを表示、編集、削除する関数
def display_schedule_list():
    for idx, schedule in enumerate(st.session_state.schedule_list):
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write(schedule["formatted_schedule"])
        new_start_time = col2.time_input("開始時刻", value=schedule["start_time"], key=f"start_{idx}")
        new_end_time = col3.time_input("終了時刻", value=schedule["end_time"], key=f"end_{idx}")
        if col4.button("更新", key=f"update_{idx}"):
            st.session_state.schedule_list[idx]["start_time"] = new_start_time
            st.session_state.schedule_list[idx]["end_time"] = new_end_time
            st.session_state.schedule_list[idx]["formatted_schedule"] = format_schedule(
                template, schedule["date"], new_start_time, new_end_time)
            st.session_state.schedule_list.sort(key=lambda x: (x['date'], x['start_time']))
        if col5.button("削除", key=f"delete_{idx}"):
            del st.session_state.schedule_list[idx]
            st.rerun()

# 出力内容を表示
st.header("スケジュール一覧")
display_schedule_list()

# スケジュールリストをクリアする関数
def reset_schedule():
    st.session_state.schedule_list = []
    st.session_state.confirmed_schedule = ""

# スケジュールを確定する関数
def confirm_schedule():
    formatted_schedules = "\n".join([item["formatted_schedule"] for item in st.session_state.schedule_list])
    st.session_state.confirmed_schedule = formatted_schedules

# 確定ボタンとリセットボタンを配置
col1, col2 = st.columns(2)
if col1.button("確定"):
    confirm_schedule()
if col2.button("リセット"):
    reset_schedule()

# 確定されたスケジュールを表示
st.header("確定スケジュール")
st.text_area("確定スケジュール", st.session_state.confirmed_schedule, height=200)

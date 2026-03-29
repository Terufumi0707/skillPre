import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Skill Runner", layout="centered")
st.title("Skill Runner (Gemini)")

with st.form("run-form"):
    user_input = st.text_area("入力", placeholder="実行したい内容を入力してください")
    skill_name = st.text_input("Skill name (optional)", placeholder="例: task-planning")
    submitted = st.form_submit_button("実行")

if submitted:
    if not user_input.strip():
        st.error("入力が空です")
    else:
        st.info("状態: 実行中")
        try:
            response = requests.post(
                f"{BACKEND_URL}/run",
                json={"user_input": user_input, "skill_name": skill_name or None},
                timeout=120,
            )
            data = response.json()

            st.subheader("実行ログ")
            for log in data.get("logs", []):
                st.write(f"- {log}")

            st.subheader("最終出力")
            if data.get("output"):
                st.write(data["output"])

            if data.get("error"):
                st.error(data["error"])
            else:
                st.success("状態: 完了")
        except Exception as exc:  # noqa: BLE001
            st.error(f"通信エラー: {exc}")

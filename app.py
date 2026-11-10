import streamlit as st
import random

st.set_page_config(page_title="計算ルーレット", layout="centered")

# スタイリッシュな見た目にするCSS（ヘッダー・フッター隠し）
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 600px;
    }
    .question-box {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 2px solid #e9ecef;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

st.title("🧮 計算ルーレット")

# ─── 難易度・ジャンル設定 ───
level = st.selectbox(
    "難易度を選択",
    ["小1〜2（たしざん・ひきざん）", "小3〜4（あまりのないわりざん・大きな数）", "小5〜6（小数・分数・四則混じる）", "中1（正負の数・文字式）"],
    label_visibility="collapsed"
)

# 問題生成ロジック
def generate_question(selected_level):
    if "小1〜2" in selected_level:
        op = random.choice(["+", "-"])
        if op == "+":
            a, b = random.randint(1, 20), random.randint(1, 20)
            ans = a + b
        else:
            a = random.randint(2, 30)
            b = random.randint(1, a)
            ans = a - b
        expr = f"{a} {op} {b}"

    elif "小3〜4" in selected_level:
        op = random.choice(["+", "-", "×", "÷"])
        if op == "+":
            a, b = random.randint(10, 99), random.randint(10, 99)
            ans = a + b
        elif op == "-":
            a = random.randint(20, 100)
            b = random.randint(1, a)
            ans = a - b
        elif op == "×":
            a, b = random.randint(2, 9), random.randint(2, 9)
            ans = a * b
        else: # ÷
            b = random.randint(2, 9)
            ans = random.randint(1, 9)
            a = b * ans
        expr = f"{a} {op} {b}"

    elif "小5〜6" in selected_level:
        op = random.choice(["小数の計算", "かっこ付き"])
        if op == "小数の計算":
            a = round(random.uniform(1.0, 9.9), 1)
            b = round(random.uniform(1.0, 9.9), 1)
            ans = round(a + b, 1)
            expr = f"{a} + {b}"
        else:
            a, b, c = random.randint(2, 9), random.randint(1, 5), random.randint(1, 5)
            ans = a * (b + c)
            expr = f"{a} × ({b} + {c})"

    else: # 中1レベル
        op = random.choice(["正負の数", "一次方程式"])
        if op == "正負の数":
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
            while a == 0 or b == 0:
                a, b = random.randint(-10, 10), random.randint(-10, 10)
            ans = a + b
            b_str = f"({b})" if b < 0 else f"{b}"
            expr = f"{a} + {b_str}"
        else:
            x = random.randint(-5, 9)
            while x == 0: x = random.randint(-5, 9)
            a = random.randint(2, 5)
            b = random.randint(1, 10)
            c = a * x + b
            b_str = f"+ {b}" if b > 0 else f"- {abs(b)}"
            ans = x
            expr = f"{a}x {b_str} = {c}  (x=?)"

    return expr, str(ans)

# ─── セッション状態の管理 ───
if "current_level" not in st.session_state or st.session_state.current_level != level:
    st.session_state.current_level = level
    expr, ans = generate_question(level)
    st.session_state.expr = expr
    st.session_state.ans = ans
    st.session_state.status = "guessing"

def next_q():
    expr, ans = generate_question(st.session_state.current_level)
    st.session_state.expr = expr
    st.session_state.ans = ans
    st.session_state.status = "guessing"

# ─── 問題表示 ───
st.markdown(f'<div class="question-box">{st.session_state.expr} = ?</div>', unsafe_allow_html=True)

# ─── 回答・操作セクション ───
if st.session_state.status == "correct":
    st.success(f"⭕️ 正解！ 答え: {st.session_state.ans}")
    if st.button("次の問題へ", use_container_width=True, type="primary"):
        next_q()
        st.rerun()

elif st.session_state.status == "revealed":
    st.info(f"💡 答え: {st.session_state.ans}")
    if st.button("次の問題へ", use_container_width=True, type="primary"):
        next_q()
        st.rerun()

else:
    with st.form(key="calc_form", clear_on_submit=True):
        user_input = st.text_input("答えを入力", placeholder="例: 15 / -3", label_visibility="collapsed")
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("回答する", use_container_width=True)
        with col2:
            giveup = st.form_submit_button("答えを見る", use_container_width=True)

    if submit and user_input:
        if user_input.strip() == st.session_state.ans:
            st.session_state.status = "correct"
            st.rerun()
        else:
            st.error(f"❌ 不正解！「{user_input}」ではありません。")

    if giveup:
        st.session_state.status = "revealed"
        st.rerun()

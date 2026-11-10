import streamlit as st
import random

st.set_page_config(page_title="計算ルーレット", layout="centered")

# ─── スタイリッシュ＆視認性重視のカスタムCSS ───
custom_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 650px;
    }
    
    /* 黒背景・白文字の問題表示ボックス */
    .question-card {
        background-color: #111111;
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        padding: 35px 20px;
        border-radius: 8px;
        margin: 20px 0;
        letter-spacing: 2px;
        border: 1px solid #333333;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* 回答表示ボックス */
    .answer-card {
        background-color: #1e293b;
        color: #38bdf8;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        padding: 25px 20px;
        border-radius: 8px;
        margin: 20px 0;
        border: 1px solid #0284c7;
        letter-spacing: 1.5px;
    }
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

st.title("計算ルーレット")

# ─── 設定パネル ───
with st.expander("計算設定", expanded=True):
    col_config1, col_config2 = st.columns(2)
    with col_config1:
        digits = st.slider("桁数", min_value=1, max_value=6, value=5)
    with col_config2:
        operations = st.multiselect(
            "演算子",
            options=["＋", "－", "×", "÷"],
            default=["＋", "－"]
        )

if not operations:
    st.warning("演算子を1つ以上選択してください。")
    st.stop()

# ─── 四則演算の自動生成ロジック ───
def generate_arithmetic_question(digits, ops):
    op = random.choice(ops)
    min_val = 10 ** (digits - 1) if digits > 1 else 1
    max_val = (10 ** digits) - 1

    if op == "＋":
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        ans = a + b
        expr = f"{a:,} ＋ {b:,}"
    elif op == "－":
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        if a < b:
            a, b = b, a
        ans = a - b
        expr = f"{a:,} － {b:,}"
    elif op == "×":
        a = random.randint(min_val, max_val)
        # かけ算は桁数が大きくなりすぎないよう調整
        b_max = 99 if digits > 3 else max_val
        b_min = 2 if digits > 3 else min_val
        b = random.randint(b_min, b_max)
        ans = a * b
        expr = f"{a:,} × {b:,}"
    else: # ÷
        b = random.randint(2, 99 if digits > 3 else 9)
        ans_val = random.randint(min_val, max_val // max(b, 1) + 1)
        a = b * ans_val
        ans = ans_val
        expr = f"{a:,} ÷ {b:,}"

    return expr, f"{ans:,}"

# 設定変更時のセッションリセット
config_key = f"{digits}_{sorted(operations)}"
if "config_key" not in st.session_state or st.session_state.config_key != config_key:
    st.session_state.config_key = config_key
    expr, ans = generate_arithmetic_question(digits, operations)
    st.session_state.expr = expr
    st.session_state.ans = ans
    st.session_state.revealed = False

def next_question():
    expr, ans = generate_arithmetic_question(digits, operations)
    st.session_state.expr = expr
    st.session_state.ans = ans
    st.session_state.revealed = False

# ─── 問題表示エリア（黒背景・白文字） ───
st.markdown(f'<div class="question-card">{st.session_state.expr} ＝ ？</div>', unsafe_allow_html=True)

# ─── ボタン操作 ───
if not st.session_state.revealed:
    if st.button("答えを確認する", use_container_width=True, type="primary"):
        st.session_state.revealed = True
        st.rerun()
else:
    st.markdown(f'<div class="answer-card">答え： {st.session_state.ans}</div>', unsafe_allow_html=True)
    if st.button("次の問題へ進む", use_container_width=True, type="primary"):
        next_question()
        st.rerun()

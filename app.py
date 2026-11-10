import streamlit as st
import random
import math

st.set_page_config(page_title="ハイパー計算トレーナー", layout="centered")

# スタイリッシュなデザインCSS
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 650px;
    }
    .question-box {
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 12px;
        margin: 20px 0;
        border: 2px solid #e9ecef;
        letter-spacing: 1px;
    }
    .answer-box {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        color: #2e7d32;
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        border: 2px solid #c8e6c9;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

st.title("🧮 ハイパー計算トレーナー")

# ─── 難易度設定 ───
level = st.selectbox(
    "難易度を選択",
    ["🔥 5桁の巨大な数の四則演算 (5桁+5桁 / 5桁-5桁)", "⚡ 中学数学（平方根・二次方程式の解）", "🚀 高度な数式・分数・複合計算"],
    label_visibility="collapsed"
)

# 難問生成ロジック
def generate_hard_question(selected_level):
    if "5桁の巨大な数" in selected_level:
        op = random.choice(["+", "-", "×"])
        if op == "+":
            a = random.randint(10000, 99999)
            b = random.randint(10000, 99999)
            ans = f"{a + b:,}"
            expr = f"{a:,} ＋ {b:,}"
        elif op == "-":
            a = random.randint(20000, 99999)
            b = random.randint(10000, a)
            ans = f"{a - b:,}"
            expr = f"{a:,} － {b:,}"
        else: # 4桁 × 2桁 または 3桁
            a = random.randint(1000, 9999)
            b = random.randint(111, 999)
            ans = f"{a * b:,}"
            expr = f"{a:,} × {b:,}"

    elif "中学数学" in selected_level:
        sub = random.choice(["quadratic", "radical"])
        if sub == "quadratic":
            # 二次方程式の解: x^2 - (p+q)x + pq = 0
            p = random.randint(-5, 5)
            q = random.randint(-5, 5)
            while p == q or p == 0 or q == 0:
                p, q = random.randint(-5, 5), random.randint(-5, 5)
            b_coef = -(p + q)
            c_coef = p * q
            b_str = f"+ {b_coef}x" if b_coef > 0 else f"- {abs(b_coef)}x" if b_coef < 0 else ""
            c_str = f"+ {c_coef}" if c_coef > 0 else f"- {abs(c_coef)}" if c_coef < 0 else ""
            expr = f"x^2 {b_str} {c_str} = 0 の解"
            ans = f"x = {min(p, q)}, {max(p, q)}"
        else:
            # 平方根の計算 (例: √48 + √27)
            bases = [2, 3, 5]
            base = random.choice(bases)
            m1 = random.randint(2, 4)
            m2 = random.randint(2, 4)
            v1 = (m1**2) * base
            v2 = (m2**2) * base
            expr = f"\\sqrt{{{v1}}} ＋ \\sqrt{{{v2}}}"
            total_m = m1 + m2
            ans = f"{total_m}\\sqrt{{{base}}}"
            
    else: # 高度な分数・複合
        d = random.choice([6, 8, 12, 15])
        n1 = random.randint(1, d-1)
        n2 = random.randint(1, d-1)
        expr = f"\\frac{{{n1}}}{{{{ {d} }}}} ＋ \\frac{{{n2}}}{{{{ {d} }}}}"
        num = n1 + n2
        g = math.gcd(num, d)
        if d // g == 1:
            ans = str(num // g)
        else:
            ans = f"\\frac{{{num//g}}}{{{{ {d//g} }}}}"

    return expr, ans

# ─── セッション状態の管理 ───
if "current_level" not in st.session_state or st.session_state.current_level != level:
    st.session_state.current_level = level
    expr, ans = generate_hard_question(level)
    st.session_state.expr = expr
    st.session_state.ans = ans
    st.session_state.revealed = False

def next_q():
    expr, ans = generate_hard_question(st.session_state.current_level)
    st.session_state.expr = expr
    st.session_state.ans = ans
    st.session_state.revealed = False

# ─── 画面描画 ───
st.markdown("問題を見て頭の中で計算し、**「答えを確認する」**ボタンを押してください。")

# 問題の表示（LaTeX数式が含まれる場合は綺麗にレンダリング）
if "\\" in st.session_state.expr:
    st.markdown(f"<div class='question-box'>", unsafe_allow_html=True)
    st.latex(st.session_state.expr)
    st.markdown(f"</div>", unsafe_allow_html=True)
else:
    st.markdown(f'<div class="question-box">{st.session_state.expr} ＝ ？</div>', unsafe_allow_html=True)

# ─── アクション部分 ───
if not st.session_state.revealed:
    if st.button("👁️ 答えを確認する", use_container_width=True, type="primary"):
        st.session_state.revealed = True
        st.rerun()
else:
    # 答えの表示
    if "\\" in st.session_state.ans:
        st.markdown(f"<div class='answer-box'>答え：", unsafe_allow_html=True)
        st.latex(st.session_state.ans)
        st.markdown(f"</div>", unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="answer-box">答え： {st.session_state.ans}</div>', unsafe_allow_html=True)
        
    if st.button("🔄 次の問題へ進む", use_container_width=True, type="primary"):
        next_q()
        st.rerun()

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="이커머스 대시보드", layout="wide")

st.title("🛒 이커머스 실시간 현황")

# Mock Data Generation
@st.cache_data
def load_data():
    dates = pd.date_range(start='2024-01-01', periods=30)
    data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.randint(100, 500, size=30) * 10000,
        'Visitors': np.random.randint(50, 200, size=30),
        'Orders': np.random.randint(10, 50, size=30)
    })
    return data

df = load_data()

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 매출", f"₩{df['Sales'].sum():,}", "+12%")
col2.metric("총 주문", f"{df['Orders'].sum()}건", "+5%")
col3.metric("방문자 수", f"{df['Visitors'].sum()}명", "+18%")
col4.metric("재고 부족 알림", "3건", "-2%", delta_color="inverse")

# Charts
col_charts_1, col_charts_2 = st.columns(2)

with col_charts_1:
    st.subheader("일별 매출 추이")
    chart_sales = alt.Chart(df).mark_line(point=True).encode(
        x='Date',
        y='Sales',
        tooltip=['Date', 'Sales']
    ).interactive()
    st.altair_chart(chart_sales, use_container_width=True)

with col_charts_2:
    st.subheader("카테고리별 판매 비중")
    categories = pd.DataFrame({
        'Category': ['Electronics', 'Clothing', 'Home', 'Books'],
        'Value': [45, 30, 15, 10]
    })
    chart_cat = alt.Chart(categories).mark_arc().encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Category", type="nominal"),
        tooltip=['Category', 'Value']
    )
    st.altair_chart(chart_cat, use_container_width=True)

# Data Table
st.subheader("최근 주문 내역")
st.dataframe(df.tail(5).sort_values(by='Date', ascending=False), use_container_width=True)

st.sidebar.info("이 대시보드는 Python Streamlit으로 제작되었습니다.")

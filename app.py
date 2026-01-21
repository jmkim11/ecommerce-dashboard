import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

st.set_page_config(page_title="이커머스 대시보드", layout="wide")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    date_range = st.date_input(
        "날짜 범위 선택",
        (datetime.now() - timedelta(days=30), datetime.now())
    )
    category_filter = st.multiselect(
        "카테고리 필터",
        ["Electronics", "Clothing", "Home", "Books", "Beauty", "Sports"],
        default=["Electronics", "Clothing"]
    )
    st.info("💡 이 대시보드는 Python Streamlit으로 제작되었습니다.")

st.title("🛒 이커머스 통합 대시보드")

# Mock Data Generation
@st.cache_data
def load_data():
    dates = pd.date_range(start='2024-01-01', periods=60)
    
    # 1. Sales Data
    sales_data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.randint(100, 500, size=60) * 10000,
        'Visitors': np.random.randint(50, 300, size=60),
        'Orders': np.random.randint(10, 80, size=60)
    })
    
    # 2. Product/Inventory Data
    categories = ["Electronics", "Clothing", "Home", "Books", "Beauty", "Sports"]
    products = []
    for i in range(50):
        cat = np.random.choice(categories)
        stock = np.random.randint(0, 100)
        status = "In Stock"
        if stock == 0: status = "Out of Stock"
        elif stock < 10: status = "Low Stock"
        
        products.append({
            "Product ID": f"P-{1000+i}",
            "Name": f"{cat} Product {i+1}",
            "Category": cat,
            "Price": np.random.randint(10, 500) * 1000,
            "Stock": stock,
            "Status": status
        })
    inventory_df = pd.DataFrame(products)
    
    return sales_data, inventory_df

df_sales, df_inventory = load_data()

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 통합 개요 (Overview)", "📦 재고 관리 (Inventory)", "📈 고객 분석 (Analytics)"])

# 1. Overview Tab
with tab1:
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    total_sales = df_sales['Sales'].sum()
    total_orders = df_sales['Orders'].sum()
    total_visitors = df_sales['Visitors'].sum()
    low_stock = len(df_inventory[df_inventory['Status'] == 'Low Stock'])
    
    col1.metric("총 매출", f"₩{total_sales:,}", "+12%")
    col2.metric("총 주문", f"{total_orders}건", "+5%")
    col3.metric("방문자 수", f"{total_visitors}명", "+18%")
    col4.metric("재고 부족 알림", f"{low_stock}건", "-2%", delta_color="inverse")
    
    # Main Charts
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("일별 매출 추이")
        chart_sales = alt.Chart(df_sales).mark_area(
            line={'color':'#4c78a8'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#4c78a8', offset=0),
                       alt.GradientStop(color='white', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            )
        ).encode(
            x='Date',
            y='Sales',
            tooltip=['Date', 'Sales']
        ).interactive()
        st.altair_chart(chart_sales, use_container_width=True)
    
    with c2:
        st.subheader("카테고리별 매출 비중")
        cat_sales = df_inventory.groupby('Category')['Price'].sum().reset_index()
        chart_pie = alt.Chart(cat_sales).mark_arc(innerRadius=50).encode(
            theta='Price',
            color='Category',
            tooltip=['Category', 'Price']
        )
        st.altair_chart(chart_pie, use_container_width=True)

# 2. Inventory Tab
with tab2:
    st.subheader("실시간 재고 현황")
    
    # Filter by Status
    status_filter = st.multiselect("상태 필터", ["In Stock", "Low Stock", "Out of Stock"], default=["Low Stock", "Out of Stock"])
    
    filtered_inventory = df_inventory[df_inventory['Status'].isin(status_filter)]
    
    # Display Table with formatting
    st.dataframe(
        filtered_inventory,
        use_container_width=True,
        column_config={
            "Price": st.column_config.NumberColumn("가격", format="₩%d"),
            "Stock": st.column_config.ProgressColumn("재고 수량", min_value=0, max_value=100, format="%d개"),
            "Status": st.column_config.TextColumn("상태")
        }
    )
    
    # Inventory Download
    st.download_button(
        "재고 목록 다운로드 (CSV)",
        df_inventory.to_csv(index=False).encode('utf-8'),
        "inventory_report.csv",
        "text/csv"
    )

# 3. Analytics Tab
with tab3:
    st.subheader("방문자 및 전환율 분석")
    
    # Scatter Plot: Visitors vs Sales
    scatter = alt.Chart(df_sales).mark_circle(size=60).encode(
        x='Visitors',
        y='Sales',
        color='Orders',
        tooltip=['Date', 'Visitors', 'Sales', 'Orders']
    ).interactive()
    
    st.altair_chart(scatter, use_container_width=True)
    
    st.write("💡 **인사이트**: 방문자 수가 증가할수록 매출도 비례하여 증가하는 경향을 보입니다. 마케팅 캠페인을 통해 유입을 늘리는 것이 중요합니다.")

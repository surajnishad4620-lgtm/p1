import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu


# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="DMart Product Analysis Dashboard",
    page_icon="🛒",
    layout="wide"
)


# ---------------------------------
# Load Dataset
# ---------------------------------

df = pd.read_csv("data.csv")


# ---------------------------------
# Data Cleaning
# ---------------------------------

# Remove completely empty rows
df.dropna(
    how="all",
    inplace=True
)


# Remove duplicate rows
df.drop_duplicates(
    inplace=True
)


# Convert Price column

df["Price"] = (
    df["Price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Price"] = pd.to_numeric(
    df["Price"],
    errors="coerce"
)



# Convert Discount column

df["Discount"] = (
    df["Discount"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace("%", "", regex=False)
    .str.replace(",", "", regex=False)
)


df["Discount"] = pd.to_numeric(
    df["Discount"],
    errors="coerce"
)



# Fill missing text values

text_columns = [
    "Name",
    "Brand",
    "Category",
    "SubCategory",
    "Quantity",
    "Description",
    "BreadCrumbs"
]


for col in text_columns:

    df[col] = (
        df[col]
        .fillna("Unknown")
    )



# Fill missing numeric values

df["Price"] = (
    df["Price"]
    .fillna(
        df["Price"].median()
    )
)


df["Discount"] = (
    df["Discount"]
    .fillna(
        df["Price"]
    )
)



# Create new columns

df["Savings"] = (
    df["Price"] - df["Discount"]
)


df["Discount %"] = (
    ((df["Price"] - df["Discount"])
    / df["Price"]) * 100
)


# Remove infinity values

df.replace(
    [float("inf"), -float("inf")],
    0,
    inplace=True
)


# Final reset index

df.reset_index(
    drop=True,
    inplace=True
)


# ---------------------------------
# Feature Engineering
# ---------------------------------

# Assuming Discount column is discounted price

df["Savings"] = df["Price"] - df["Discount"]


df["Discount %"] = (
    ((df["Price"] - df["Discount"])
     / df["Price"]) * 100
).round(2)


df["Discount %"] = (
    df["Discount %"]
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0)
)



# ---------------------------------
# Sidebar
# ---------------------------------

with st.sidebar:


    st.image(
        "dmart3.webp",
        width=220
    )


    opt = option_menu(
        "Menu",
        [
            "Home",
            "Dataset",
            "Visualization",
            "About"
        ],

        icons=[
            "house",
            "table",
            "bar-chart",
            "person"
        ],

        default_index=0
    )


    st.markdown("---")


    # Category Filter

    category = st.selectbox(
        "Select Category",
        [
            "All"
        ] +
        sorted(
            df["Category"]
            .dropna()
            .unique()
            .tolist()
        )
    )


    if category != "All":

        df = df[
            df["Category"] == category
        ]



    # Brand Filter

    brand = st.selectbox(
        "Select Brand",
        [
            "All"
        ] +
        sorted(
            df["Brand"]
            .dropna()
            .unique()
            .tolist()
        )
    )


    if brand != "All":

        df = df[
            df["Brand"] == brand
        ]



# ==========================
# HOME PAGE
# ==========================

if opt == "Home":


    st.title(
        "🛒 DMart Product Analysis Dashboard"
    )


    c1,c2,c3,c4,c5 = st.columns(5)


    c1.metric(
        "Total Products",
        len(df)
    )


    c2.metric(
        "Brands",
        df["Brand"].nunique()
    )


    c3.metric(
        "Categories",
        df["Category"].nunique()
    )


    c4.metric(
        "Sub Categories",
        df["SubCategory"].nunique()
    )


    c5.metric(
        "Average Price",
        f"₹ {round(df['Price'].mean(),2)}"
    )



    st.divider()



    search = st.text_input(
        "🔍 Search Product"
    )


    if search:


        result = df[
            df["Name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


        st.dataframe(
            result,
            use_container_width=True
        )



    st.info(
        """
        ### Dashboard Features

        ✔ Product Analysis  
        ✔ Category Analysis  
        ✔ Brand Analysis  
        ✔ Price Analysis  
        ✔ Discount Analysis  
        ✔ Savings Analysis  
        ✔ Interactive Visualizations
        """
    )



# ==========================
# DATASET PAGE
# ==========================


elif opt == "Dataset":


    tab1,tab2,tab3 = st.tabs(
        [
            "Dataset",
            "Columns",
            "Statistics"
        ]
    )



    with tab1:


        st.dataframe(
            df,
            use_container_width=True
        )



    with tab2:


        st.write(
            df.columns.tolist()
        )



    with tab3:


        st.dataframe(
            df.describe(include="all"),
            use_container_width=True
        )
# ==========================
# VISUALIZATION PAGE
# ==========================

elif opt == "Visualization":


    tabs = st.tabs(
        [
            "Category",
            "Brand",
            "Price",
            "Discount",
            "SubCategory",
            "Quantity",
            "Top Products",
            "Scatter",
            "Pie Chart"
        ]
    )


    # ---------------------------------
    # Category Analysis
    # ---------------------------------

    with tabs[0]:


        st.subheader(
            "📊 Products by Category"
        )


        category_df = (
            df["Category"]
            .value_counts()
            .reset_index()
        )


        category_df.columns = [
            "Category",
            "Products"
        ]


        fig = px.bar(
            category_df,
            x="Category",
            y="Products",
            color="Products",
            text="Products",
            template="plotly_white"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



    # ---------------------------------
    # Brand Analysis
    # ---------------------------------

    with tabs[1]:


        st.subheader(
            "🏷 Top 10 Brands"
        )


        brand_df = (
            df["Brand"]
            .value_counts()
            .head(10)
            .reset_index()
        )


        brand_df.columns = [
            "Brand",
            "Products"
        ]



        fig = px.bar(
            brand_df,
            x="Brand",
            y="Products",
            color="Products",
            text="Products",
            template="plotly_white"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



    # ---------------------------------
    # Price Distribution
    # ---------------------------------

    with tabs[2]:


        st.subheader(
            "💰 Price Distribution"
        )


        fig = px.histogram(
            df,
            x="Price",
            nbins=40,
            color_discrete_sequence=[
                "green"
            ],
            template="plotly_white"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



    # ---------------------------------
    # Discount Analysis
    # ---------------------------------

    with tabs[3]:


        st.subheader(
            "🔥 Discount Distribution"
        )


        fig = px.histogram(
            df,
            x="Discount %",
            nbins=30,
            color_discrete_sequence=[
                "orange"
            ],
            template="plotly_white"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



    # ---------------------------------
    # SubCategory Analysis
    # ---------------------------------

    with tabs[4]:


        st.subheader(
            "📦 Top Sub Categories"
        )


        sub_df = (
            df["SubCategory"]
            .value_counts()
            .head(15)
            .reset_index()
        )


        sub_df.columns = [
            "SubCategory",
            "Products"
        ]



        fig = px.bar(
            sub_df,
            x="SubCategory",
            y="Products",
            color="Products",
            text="Products",
            template="plotly_white"
        )


        fig.update_layout(
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



    # ---------------------------------
    # Quantity Analysis
    # ---------------------------------

    with tabs[5]:


        st.subheader(
            "📦 Quantity Distribution"
        )


        qty_df = (
            df["Quantity"]
            .value_counts()
            .head(20)
            .reset_index()
        )


        qty_df.columns = [
            "Quantity",
            "Products"
        ]



        fig = px.bar(
            qty_df,
            x="Quantity",
            y="Products",
            color="Products",
            text="Products",
            template="plotly_white"
        )


        fig.update_layout(
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



    # ---------------------------------
    # Expensive Products
    # ---------------------------------

    with tabs[6]:


        st.subheader(
            "💎 Top 10 Expensive Products"
        )


        top_products = (
            df.sort_values(
                "Price",
                ascending=False
            )
            .head(10)
        )



        fig = px.bar(
            top_products,
            x="Name",
            y="Price",
            color="Price",
            text="Price",
            template="plotly_white"
        )


        fig.update_layout(
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



    # ---------------------------------
    # Scatter Plot
    # ---------------------------------

    with tabs[7]:


        st.subheader(
            "📈 Price vs Discount"
        )


        fig = px.scatter(
            df,
            x="Price",
            y="Discount %",
            color="Category",
            size="Savings",
            hover_name="Name",
            template="plotly_white"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )




    # ---------------------------------
    # Pie Chart
    # ---------------------------------

    with tabs[8]:


        st.subheader(
            "🥧 Category Share"
        )


        fig = px.pie(
            df,
            names="Category",
            hole=0.4,
            template="plotly_white"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )
#     tabs = st.tabs(
#         [
#             "Category",
#             "Brand",
#             "Price",
#             "Discount",
#             "SubCategory",
#             "Quantity",
#             "Top Products",
#             "Scatter",
#             "Treemap",
#             "Pie Chart",
#             "Average Price",
#             "Brand Price",
#             "Savings",
#             "Country",
#             "Sunburst",
#             "Box Plot",
#             "Violin Plot",
#             "Heatmap",
#             "Brand Heatmap",
#             "Line Chart"
#         ]
# )

# ==========================
# ABOUT PAGE
# ==========================

elif opt == "About":
    st.title(
        "🛒 About DMart Product Analysis Dashboard"
    )


    st.markdown(
        """
        ## Project Overview

        This Streamlit dashboard performs exploratory 
        data analysis on the DMart Products dataset.

        The dashboard provides insights into:

        - Product distribution
        - Brand performance
        - Category analysis
        - Pricing patterns
        - Discount analysis
        - Savings analysis
        - Product segmentation


        ## Technologies Used

        🐍 Python

        📊 Pandas

        📈 Plotly

        📉 Matplotlib

        🎨 Seaborn

        🚀 Streamlit


        ## Dataset Columns

        | Column | Description |
        |---|---|
        | Name | Product Name |
        | Brand | Product Brand |
        | Price | Original Price |
        | Discount | Discounted Price |
        | Category | Main Category |
        | SubCategory | Product Sub Category |
        | Quantity | Pack Size |
        | Description | Country/Origin |
        | BreadCrumbs | Website Category Path |


        ## Dashboard Features

        ✔ Interactive Filters

        ✔ Product Search

        ✔ KPI Cards

        ✔ Category Analysis

        ✔ Brand Analysis

        ✔ Price Analysis

        ✔ Discount Analysis

        ✔ Savings Analysis

        ✔ Advanced Charts


        ## Created For

        Data Analytics Portfolio Project
        """
    )



# ==========================
# CUSTOM CSS
# ==========================

st.markdown(
    """
    <style>

    /* Main background */

    .stApp {

        background-color:#f8f9fa;

    }


    /* Metric Cards */

    div[data-testid="metric-container"] {

        background-color:white;

        border-radius:15px;

        padding:15px;

        box-shadow:
        0px 2px 8px rgba(0,0,0,0.1);

    }


    /* Sidebar */

    section[data-testid="stSidebar"] {

        background-color:#ffffff;

    }


    /* Headers */

    h1 {

        color:#1f4e79;

        font-weight:700;

    }


    h2,h3 {

        color:#2c3e50;

    }


    /* Dataframe */

    .stDataFrame {

        border-radius:10px;

    }


    </style>
    """,
    unsafe_allow_html=True
)
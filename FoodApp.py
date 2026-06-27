import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 1. APP SETTINGS
# ==================================================

st.set_page_config(
    page_title="Food Label Intelligence App",
    page_icon="🥫",
    layout="wide"
)

st.title("Food Label Intelligence App")
st.write(
    "An interactive Python app that helps explore packaged food labels, "
    "nutrition values, allergens, additives, and simple product concern levels."
)

st.caption("Demo version using sample packaged-food label data.")


# ==================================================
# 2. CONSTANTS
# ==================================================

DATA_FILE = "sample_food_labels_50.csv"

CONCERN_COLORS = {
    "High Concern": "#C62828",
    "Medium Concern": "#F2A900",
    "Low Concern": "#9CA3AF"
}

CONCERN_ORDER = ["High Concern", "Medium Concern", "Low Concern"]
NUTRISCORE_ORDER = ["A", "B", "C", "D", "E"]


# ==================================================
# 3. LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    """Load sample food-label data from a CSV file."""
    df = pd.read_csv(DATA_FILE)
    return df


# ==================================================
# 4. SCORING FUNCTIONS
# ==================================================

def calculate_concern_score(row):
    """Calculate a simple rule-based concern score."""

    score = 0

    if row["Sugar per 100g"] >= 15:
        score += 2

    if row["Salt per 100g"] >= 1.5:
        score += 2

    if row["Saturated Fat per 100g"] >= 5:
        score += 1

    if row["Additives Count"] > 0:
        score += 1

    if row["Allergens"] not in ["", "Unknown", "Not listed"]:
        score += 2

    if row["NOVA Group"] == 4:
        score += 1

    return score


def assign_concern_level(score):
    """Convert concern score into a concern level."""

    if score >= 6:
        return "High Concern"
    elif score >= 3:
        return "Medium Concern"
    else:
        return "Low Concern"


# ==================================================
# 5. PREPARE DATA
# ==================================================

# Load the sample product data
df = load_data()

# Add score and level fields
df["Concern Score"] = df.apply(calculate_concern_score, axis=1)
df["Concern Level"] = df["Concern Score"].apply(assign_concern_level)


# ==================================================
# 6. SIDEBAR FILTERS
# ==================================================

st.sidebar.header("Filters")

search_text = st.sidebar.text_input(
    "Search product, brand, category, or ingredient"
)

category_options = sorted(df["Categories"].unique())

selected_categories = st.sidebar.multiselect(
    "Category",
    category_options,
    default=category_options
)

concern_options = [
    level for level in CONCERN_ORDER
    if level in df["Concern Level"].unique()
]

selected_concern_levels = st.sidebar.multiselect(
    "Concern Level",
    concern_options,
    default=concern_options
)

nutriscore_options = [
    score for score in NUTRISCORE_ORDER
    if score in df["Nutri-Score"].unique()
]

selected_nutriscores = st.sidebar.multiselect(
    "Nutri-Score",
    nutriscore_options,
    default=nutriscore_options
)

allergen_filter = st.sidebar.selectbox(
    "Allergen filter",
    [
        "All products",
        "Products with allergens",
        "Products without listed allergens"
    ]
)

top_n = st.sidebar.slider(
    "Number of products in top chart",
    min_value=5,
    max_value=30,
    value=10,
    step=5
)


# ==================================================
# 7. APPLY FILTERS
# ==================================================

filtered_df = df[
    (df["Categories"].isin(selected_categories)) &
    (df["Concern Level"].isin(selected_concern_levels)) &
    (df["Nutri-Score"].isin(selected_nutriscores))
].copy()

# Search across multiple text columns
if search_text:
    search_mask = (
        filtered_df["Product Name"].str.contains(search_text, case=False, na=False) |
        filtered_df["Brand"].str.contains(search_text, case=False, na=False) |
        filtered_df["Categories"].str.contains(search_text, case=False, na=False) |
        filtered_df["Ingredients"].str.contains(search_text, case=False, na=False)
    )

    filtered_df = filtered_df[search_mask]

# Apply allergen filter
if allergen_filter == "Products with allergens":
    filtered_df = filtered_df[
        ~filtered_df["Allergens"].isin(["", "Unknown", "Not listed"])
    ]

elif allergen_filter == "Products without listed allergens":
    filtered_df = filtered_df[
        filtered_df["Allergens"].isin(["", "Unknown", "Not listed"])
    ]

# Stop the app if filters remove all products
if filtered_df.empty:
    st.warning("No products match the selected filters.")
    st.stop()


# ==================================================
# 8. KPI CARDS
# ==================================================

total_products = len(filtered_df)

high_concern_products = (
    filtered_df["Concern Level"] == "High Concern"
).sum()

products_with_allergens = (
    ~filtered_df["Allergens"].isin(["", "Unknown", "Not listed"])
).sum()

average_score = filtered_df["Concern Score"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Products", total_products)
col2.metric("High Concern", high_concern_products)
col3.metric("With Allergens", products_with_allergens)
col4.metric("Avg. Concern Score", f"{average_score:.1f}")

st.divider()


# ==================================================
# 9. SUMMARY CHARTS
# ==================================================

col_left, col_right = st.columns(2)

# Chart: products by concern level
with col_left:
    concern_summary = (
        filtered_df["Concern Level"]
        .value_counts()
        .reindex(CONCERN_ORDER)
        .dropna()
        .reset_index()
    )

    concern_summary.columns = ["Concern Level", "Product Count"]

    fig_concern = px.bar(
        concern_summary,
        x="Concern Level",
        y="Product Count",
        title="Products by Concern Level",
        color="Concern Level",
        color_discrete_map=CONCERN_COLORS
    )

    st.plotly_chart(fig_concern, use_container_width=True)

# Chart: top product categories
with col_right:
    category_summary = (
        filtered_df["Categories"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    category_summary.columns = ["Category", "Product Count"]

    fig_category = px.bar(
        category_summary,
        x="Product Count",
        y="Category",
        orientation="h",
        title="Top Categories"
    )

    fig_category.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig_category, use_container_width=True)


# ==================================================
# 10. TOP PRODUCTS CHART
# ==================================================

st.subheader("Top Products by Concern Score")

top_products = (
    filtered_df
    .sort_values(by="Concern Score", ascending=False)
    .head(top_n)
)

fig_top_products = px.bar(
    top_products,
    x="Concern Score",
    y="Product Name",
    orientation="h",
    title="Top Products by Concern Score",
    color="Concern Level",
    color_discrete_map=CONCERN_COLORS
)

fig_top_products.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig_top_products, use_container_width=True)

st.divider()


# ==================================================
# 11. PRODUCT COMPARISON
# ==================================================

st.subheader("Product Comparison")

product_options = sorted(filtered_df["Product Name"].unique())

if len(product_options) >= 2:
    col_a, col_b = st.columns(2)

    with col_a:
        selected_product_1 = st.selectbox(
            "Select first product",
            product_options,
            index=0
        )

    with col_b:
        selected_product_2 = st.selectbox(
            "Select second product",
            product_options,
            index=1
        )

    product_1 = filtered_df[
        filtered_df["Product Name"] == selected_product_1
    ].iloc[0]

    product_2 = filtered_df[
        filtered_df["Product Name"] == selected_product_2
    ].iloc[0]

    # Comparison table
    comparison_columns = [
        "Concern Level",
        "Concern Score",
        "Nutri-Score",
        "NOVA Group",
        "Sugar per 100g",
        "Salt per 100g",
        "Saturated Fat per 100g",
        "Additives Count",
        "Allergens"
    ]

    comparison_table = pd.DataFrame({
        "Metric": comparison_columns,
        selected_product_1: product_1[comparison_columns].values,
        selected_product_2: product_2[comparison_columns].values
    })

    st.dataframe(
        comparison_table,
        use_container_width=True
    )

    # Comparison chart
    chart_columns = [
        "Concern Score",
        "Sugar per 100g",
        "Salt per 100g",
        "Saturated Fat per 100g",
        "Additives Count"
    ]

    comparison_chart = pd.DataFrame({
        "Metric": chart_columns,
        selected_product_1: product_1[chart_columns].values,
        selected_product_2: product_2[chart_columns].values
    })

    comparison_chart = comparison_chart.melt(
        id_vars="Metric",
        var_name="Product",
        value_name="Value"
    )

    fig_comparison = px.bar(
        comparison_chart,
        x="Metric",
        y="Value",
        color="Product",
        barmode="group",
        title="Product Nutrition & Concern Comparison"
    )

    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )

else:
    st.info("Select filters that include at least two products to compare.")

st.divider()


# ==================================================
# 12. PRODUCT DETAILS TABLE
# ==================================================

st.subheader("Product Details")

display_columns = [
    "Product Name",
    "Brand",
    "Categories",
    "Concern Level",
    "Concern Score",
    "Nutri-Score",
    "NOVA Group",
    "Sugar per 100g",
    "Salt per 100g",
    "Saturated Fat per 100g",
    "Additives Count",
    "Allergens",
    "Ingredients"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True
)


# ==================================================
# 13. SCORING EXPLANATION
# ==================================================

with st.expander("How is the concern score calculated?"):
    st.write(
        "The concern score is a simple rule-based indicator created for this portfolio project. "
        "It is based on nutrition values, allergens, additives, and processing level."
    )

    scoring_rules = pd.DataFrame({
        "Condition": [
            "Sugar per 100g >= 15",
            "Salt per 100g >= 1.5",
            "Saturated fat per 100g >= 5",
            "Additives count > 0",
            "Allergens listed",
            "NOVA Group = 4"
        ],
        "Points Added": [2, 2, 1, 1, 2, 1]
    })

    st.dataframe(scoring_rules, use_container_width=True)


# ==================================================
# 14. DISCLAIMER
# ==================================================

st.info(
    "This app uses sample food-label data for portfolio demonstration. "
    "The concern score is a simple rule-based indicator and is not medical or dietary advice."
)

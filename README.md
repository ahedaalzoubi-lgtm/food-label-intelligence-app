# Food Label Intelligence App

An interactive Python and Streamlit app for exploring packaged food labels, nutrition values, allergens, additives, and simple product concern levels.

This project was created as part of my transition into data analysis, combining Python app development with my background in nutrition, food safety, label review, and compliance thinking.

## Project Objective

The objective of this app is to help users explore packaged food products in a simple, interactive way and understand key label-related information such as:

* Nutrition values
* Allergens
* Additives
* Nutri-Score
* NOVA processing group
* Simple product concern level
* Product comparison across key label indicators

## App Features

The app includes:

* Search by product name, brand, category, or ingredient
* Category filter
* Concern level filter
* Nutri-Score filter
* Allergen filter
* KPI cards for product count, high-concern products, products with allergens, and average concern score
* Bar chart showing products by concern level
* Bar chart showing top product categories
* Top products by concern score
* Product comparison table and chart
* Product details table
* Scoring explanation section

## Dataset

This project uses a sample packaged-food label dataset created for portfolio demonstration purposes.

The dataset includes product-level information such as:

* Product name
* Brand
* Category
* Ingredients
* Allergens
* Additives count
* Nutri-Score
* NOVA group
* Sugar per 100g
* Salt per 100g
* Saturated fat per 100g
* Energy kcal per 100g

The sample dataset is included in this repository as:

`sample_food_labels_50.csv`

## Concern Score Logic

The concern score is a simple rule-based indicator. It is not a medical, dietary, or regulatory assessment.

The score is calculated using the following rules:

| Condition                   | Points Added |
| --------------------------- | -----------: |
| Sugar per 100g >= 15        |            2 |
| Salt per 100g >= 1.5        |            2 |
| Saturated fat per 100g >= 5 |            1 |
| Additives count > 0         |            1 |
| Allergens listed            |            2 |
| NOVA Group = 4              |            1 |

The final score is grouped into:

* High Concern
* Medium Concern
* Low Concern

## Tools Used

* Python
* Streamlit
* pandas
* Plotly

## How to Run the App

1. Clone or download this repository.
2. Make sure the following files are in the same folder:

```text
FoodApp.py
sample_food_labels_50.csv
requirements.txt
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run FoodApp.py
```

## Project Note

This app is for portfolio and educational purposes only. It uses sample food-label data and a simple rule-based scoring method. The concern score should not be interpreted as medical advice, dietary advice, or an official food safety classification.

## Future Improvements

Future improvements could include:

* Connecting the app to a live food product database such as Open Food Facts
* Adding barcode-based product lookup
* Expanding the dataset with more real packaged-food products
* Adding clearer allergen category grouping
* Adding a product image preview
* Adding export options for filtered product tables
* Improving the scoring logic using official nutrition profiling guidelines
* Adding more advanced comparison features between similar products

## Key Skills Demonstrated

This project demonstrates:

* Building an interactive Python app using Streamlit
* Loading and analyzing structured CSV data
* Creating user filters and search functionality
* Applying rule-based scoring logic
* Creating KPI cards and interactive charts
* Designing a simple product comparison feature
* Translating food label and nutrition knowledge into a practical data app

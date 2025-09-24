# scripts/generate_products_2025.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(2025)
random.seed(2025)

def generate_products_2025(num_products=2000):
    """Génère des données produits pour 2025"""
    
    print(f"�� Generating {num_products} products for 2025...")
    
    # Catégories et sous-catégories 2025
    categories = {
        'Electronics': {
            'subcategories': ['Smartphones', 'Laptops', 'Tablets', 'Headphones', 'Smart Home', 'Gaming'],
            'price_ranges': {'min': 50, 'max': 3000},
            'brands': ['Apple', 'Samsung', 'Sony', 'Microsoft', 'Google', 'Dell', 'HP']
        },
        'Fashion': {
            'subcategories': ['Clothing', 'Shoes', 'Accessories', 'Bags', 'Jewelry', 'Watches'],
            'price_ranges': {'min': 20, 'max': 800},
            'brands': ['Nike', 'Adidas', 'Zara', 'H&M', 'Gucci', 'Prada', 'Uniqlo']
        },
        'Home & Garden': {
            'subcategories': ['Furniture', 'Decor', 'Kitchen', 'Lighting', 'Garden', 'Tools'],
            'price_ranges': {'min': 15, 'max': 1500},
            'brands': ['IKEA', 'West Elm', 'CB2', 'Williams Sonoma', 'Home Depot', 'Lowes']
        },
        'Books': {
            'subcategories': ['Fiction', 'Non-Fiction', 'Educational', 'Comics', 'Children', 'E-books'],
            'price_ranges': {'min': 8, 'max': 60},
            'brands': ['Penguin', 'Random House', 'HarperCollins', 'Scholastic', 'Marvel', 'DC']
        },
        'Sports': {
            'subcategories': ['Fitness', 'Outdoor', 'Team Sports', 'Individual Sports', 'Water Sports'],
            'price_ranges': {'min': 25, 'max': 1200},
            'brands': ['Nike', 'Adidas', 'Under Armour', 'Patagonia', 'North Face', 'REI']
        },
        'Health & Beauty': {
            'subcategories': ['Skincare', 'Makeup', 'Supplements', 'Personal Care', 'Wellness'],
            'price_ranges': {'min': 10, 'max': 300},
            'brands': ['L\'Oreal', 'Nivea', 'Clinique', 'The Body Shop', 'Sephora', 'Ulta']
        }
    }
    
    products = []
    
    for i in range(num_products):
        # Sélection de catégorie
        category = random.choice(list(categories.keys()))
        subcategory = random.choice(categories[category]['subcategories'])
        brand = random.choice(categories[category]['brands'])
        
        # Génération du nom du produit
        product_adjectives = ['Pro', 'Max', 'Ultra', 'Premium', 'Elite', 'Smart', 'Advanced', 'Classic']
        product_name = f"{brand} {subcategory} {random.choice(product_adjectives)} 2025"
        
        # ID et SKU
        product_id = f"PROD-2025-{i+1:06d}"
        sku = f"{brand[:3].upper()}-{category[:3].upper()}-{i+1:04d}"
        
        # Prix basé sur la catégorie et ajustement pour 2025 (inflation)
        base_price = np.random.uniform(
            categories[category]['price_ranges']['min'],
            categories[category]['price_ranges']['max']
        )
        # Ajustement inflation 2025 (+5-8%)
        inflation_factor = np.random.uniform(1.05, 1.08)
        price = round(base_price * inflation_factor, 2)
        
        # Coût (60-80% du prix de vente)
        cost = round(price * np.random.uniform(0.60, 0.80), 2)
        
        # Stock et popularité
        stock_quantity = np.random.randint(10, 500)
        
        # Tendances 2025 : certains produits sont plus populaires
        if any(keyword in product_name.lower() for keyword in ['smart', 'ai', 'eco', 'sustainable']):
            popularity_boost = 1.5
        else:
            popularity_boost = 1.0
        
        avg_rating = min(5.0, np.random.normal(4.2, 0.5) * popularity_boost)
        num_reviews = max(0, int(np.random.exponential(50) * popularity_boost))
        
        # Dates
        launch_date = datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 365))
        
        # Caractéristiques 2025
        is_eco_friendly = random.random() > 0.7  # 30% des produits sont éco-friendly
        is_ai_enabled = category == 'Electronics' and random.random() > 0.6  # 40% des electronics ont de l'IA
        is_bestseller = avg_rating > 4.5 and num_reviews > 100
        
        # Dimensions (pour shipping)
        weight = round(np.random.uniform(0.1, 10.0), 2)
        
        product = {
            'product_id': product_id,
            'sku': sku,
            'product_name': product_name,
            'category': category,
            'subcategory': subcategory,
            'brand': brand,
            'price': price,
            'cost': cost,
            'stock_quantity': stock_quantity,
            'avg_rating': round(avg_rating, 2),
            'num_reviews': num_reviews,
            'launch_date': launch_date,
            'weight': weight,
            'is_eco_friendly': is_eco_friendly,
            'is_ai_enabled': is_ai_enabled,
            'is_bestseller': is_bestseller,
            'created_at': datetime(2025, 1, 1),
            'updated_at': launch_date
        }
        
        products.append(product)
        
        if (i + 1) % 200 == 0:
            print(f"  Generated {i + 1} products...")
    
    df = pd.DataFrame(products)
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs('data', exist_ok=True)
    
    output_path = 'data/products_2025.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Products data saved to {output_path}")
    print(f"📊 Summary:")
    print(f"  - Total products: {len(df)}")
    print(f"  - Category distribution:")
    for category in categories.keys():
        count = len(df[df['category'] == category])
        percentage = (count / len(df)) * 100
        print(f"    {category}: {count} ({percentage:.1f}%)")
    print(f"  - Average price: ${df['price'].mean():.2f}")
    print(f"  - Eco-friendly products: {df['is_eco_friendly'].sum()} ({df['is_eco_friendly'].mean()*100:.1f}%)")
    
    return df

if __name__ == "__main__":
    generate_products_2025()

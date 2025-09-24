# scripts/generate_orders_2025.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid
import os

np.random.seed(2025)
random.seed(2025)

def generate_orders_2025(num_orders=50000):
    """Génère des données de commandes pour 2025"""
    
    print(f"🛒 Generating {num_orders} orders for 2025...")
    
    # Charger les données clients et produits
    try:
        customers_df = pd.read_csv('data/customers_2025.csv')
        products_df = pd.read_csv('data/products_2025.csv')
        print(f"  Loaded {len(customers_df)} customers and {len(products_df)} products")
    except FileNotFoundError:
        print("❌ Please generate customers and products data first!")
        return None
    
    orders = []
    order_items = []
    
    # Patterns de commandes par saison 2025
    seasonal_patterns = {
        'Q1': 0.8,   # Janvier-Mars : après fêtes, plus calme
        'Q2': 1.0,   # Avril-Juin : normal
        'Q3': 0.9,   # Juillet-Sept : vacances d'été
        'Q4': 1.4    # Oct-Déc : fêtes de fin d'année
    }
    
    # Méthodes de paiement 2025
    payment_methods = {
        'Credit Card': 0.45,
        'PayPal': 0.25, 
        'Apple Pay': 0.15,
        'Google Pay': 0.10,
        'Bank Transfer': 0.03,
        'Cryptocurrency': 0.02  # Nouveau en 2025
    }
    
    # Status des commandes
    order_statuses = ['Completed', 'Pending', 'Cancelled', 'Refunded']
    status_weights = [0.85, 0.08, 0.05, 0.02]
    
    for i in range(num_orders):
        # Sélection client pondérée par segment
        customer = customers_df.sample(n=1, weights=customers_df['order_frequency']).iloc[0]
        
        # Date de commande (2025)
        start_2025 = datetime(2025, 1, 1)
        end_2025 = datetime(2025, 12, 31)
        
        # Ajuster la probabilité selon la saison
        days_in_2025 = 365
        random_day = np.random.randint(0, days_in_2025)
        order_date = start_2025 + timedelta(days=random_day)
        
        # Ajustement saisonnier
        month = order_date.month
        if month <= 3:
            seasonal_factor = seasonal_patterns['Q1']
        elif month <= 6:
            seasonal_factor = seasonal_patterns['Q2']
        elif month <= 9:
            seasonal_factor = seasonal_patterns['Q3']
        else:
            seasonal_factor = seasonal_patterns['Q4']
        
        # Ignorer cette commande si elle ne passe pas le filtre saisonnier
        if np.random.random() > seasonal_factor:
            continue
        
        # Génération de l'ID de commande
        order_id = f"ORDER-2025-{i+1:08d}"
        
        # Nombre d'articles (influencé par le segment client)
        if customer['customer_segment'] == 'Enterprise':
            num_items = np.random.poisson(8) + 1
        elif customer['customer_segment'] == 'Premium':
            num_items = np.random.poisson(4) + 1
        elif customer['customer_segment'] == 'Regular':
            num_items = np.random.poisson(2) + 1
        else:  # Budget
            num_items = np.random.poisson(1) + 1
        
        num_items = min(num_items, 20)  # Max 20 articles par commande
        
        # Sélection des produits
        customer_categories = customer['preferred_categories'].split(',')
        
        # 70% chance de choisir dans les catégories préférées
        selected_products = []
        total_amount = 0
        
        for item_idx in range(num_items):
            if np.random.random() < 0.7 and customer_categories:
                # Choisir dans les catégories préférées
                category_filter = products_df['category'].isin(customer_categories)
                available_products = products_df[category_filter]
            else:
                # Choisir n'importe quel produit
                available_products = products_df
            
            if len(available_products) == 0:
                available_products = products_df
            
            # Pondérer par popularité (rating * reviews)
            weights = (available_products['avg_rating'] * 
                      np.log1p(available_products['num_reviews']) + 1)
            
            product = available_products.sample(n=1, weights=weights).iloc[0]
            quantity = np.random.randint(1, 4)  # 1-3 unités par produit
            
            # Prix avec possibles promotions
            unit_price = product['price']
            if np.random.random() < 0.15:  # 15% de chance de promotion
                discount = np.random.uniform(0.05, 0.25)  # 5-25% de réduction
                unit_price = round(unit_price * (1 - discount), 2)
            
            total_price = round(unit_price * quantity, 2)
            total_amount += total_price
            
            # Article de commande
            order_item = {
                'order_id': order_id,
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'category': product['category'],
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': total_price
            }
            
            order_items.append(order_item)
            selected_products.append(product['product_id'])
        
        # Frais de port (gratuits pour commandes > 50€ ou clients VIP)
        if total_amount > 50 or customer['is_vip']:
            shipping_cost = 0
        else:
            shipping_cost = round(np.random.uniform(3, 12), 2)
        
        total_amount += shipping_cost
        
        # Méthode de paiement
        payment_method = np.random.choice(
            list(payment_methods.keys()), 
            p=list(payment_methods.values())
        )
        
        # Status de la commande
        order_status = np.random.choice(order_statuses, p=status_weights)
        
        # Dates de traitement
        if order_status == 'Completed':
            shipped_date = order_date + timedelta(days=np.random.randint(1, 5))
            delivered_date = shipped_date + timedelta(days=np.random.randint(1, 10))
        else:
            shipped_date = None
            delivered_date = None
        
        # Canal de vente (nouveau pour 2025)
        if customer['mobile_app_user'] and np.random.random() < 0.6:
            sales_channel = 'Mobile App'
        elif np.random.random() < 0.1:
            sales_channel = 'Physical Store'
        else:
            sales_channel = 'Website'
        
        # Commande principale
        order = {
            'order_id': order_id,
            'customer_id': customer['customer_id'],
            'order_date': order_date,
            'total_amount': round(total_amount, 2),
            'shipping_cost': shipping_cost,
            'payment_method': payment_method,
            'order_status': order_status,
            'sales_channel': sales_channel,
            'num_items': len(selected_products),
            'shipped_date': shipped_date,
            'delivered_date': delivered_date,
            'created_at': order_date
        }
        
        orders.append(order)
        
        if (i + 1) % 5000 == 0:
            print(f"  Generated {i + 1} orders...")
    
    # Créer les DataFrames
    orders_df = pd.DataFrame(orders)
    order_items_df = pd.DataFrame(order_items)
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs('data', exist_ok=True)
    
    # Sauvegarder les données
    orders_output = 'data/orders_2025.csv'
    items_output = 'data/order_items_2025.csv'
    
    orders_df.to_csv(orders_output, index=False)
    order_items_df.to_csv(items_output, index=False)
    
    print(f"✅ Orders data saved to {orders_output}")
    print(f"✅ Order items data saved to {items_output}")
    print(f"📊 Summary:")
    print(f"  - Total orders: {len(orders_df)}")
    print(f"  - Total order items: {len(order_items_df)}")
    print(f"  - Average order value: ${orders_df['total_amount'].mean():.2f}")
    print(f"  - Total revenue: ${orders_df['total_amount'].sum():,.2f}")
    print(f"  - Status distribution:")
    for status in order_statuses:
        count = len(orders_df[orders_df['order_status'] == status])
        percentage = (count / len(orders_df)) * 100
        print(f"    {status}: {count} ({percentage:.1f}%)")
    
    return orders_df, order_items_df

if __name__ == "__main__":
    generate_orders_2025()

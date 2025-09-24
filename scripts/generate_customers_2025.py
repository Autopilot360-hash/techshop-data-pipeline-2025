# scripts/generate_customers_2025.py
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import uuid
import random

fake = Faker(['en_US', 'fr_FR', 'de_DE', 'es_ES'])
Faker.seed(2025)
np.random.seed(2025)

def generate_customers_2025(num_customers=10000):
    """Génère des données clients pour 2025"""
    
    print(f"🧑‍🤝‍🧑 Generating {num_customers} customers for 2025...")
    
    customers = []
    
    # Définir les segments de clients
    customer_segments = ['Premium', 'Regular', 'Budget', 'Enterprise']
    segment_weights = [0.15, 0.45, 0.30, 0.10]
    
    # Pays et régions pour 2025
    countries = {
        'US': 0.35, 'FR': 0.15, 'DE': 0.15, 'GB': 0.10, 
        'ES': 0.08, 'IT': 0.07, 'CA': 0.06, 'AU': 0.04
    }
    
    for i in range(num_customers):
        # Informations de base
        customer_id = f"CUST-2025-{i+1:06d}"
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}"
        
        # Date de création (clients créés entre 2023 et fin 2025)
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2025, 12, 31)
        created_at = fake.date_between(start_date=start_date, end_date=end_date)
        
        # Localisation
        country = np.random.choice(list(countries.keys()), p=list(countries.values()))
        
        # Segment client
        segment = np.random.choice(customer_segments, p=segment_weights)
        
        # Données comportementales basées sur le segment
        if segment == 'Premium':
            lifetime_value = np.random.normal(5000, 1500)
            avg_order_value = np.random.normal(300, 80)
            order_frequency = np.random.normal(8, 2)
        elif segment == 'Enterprise':
            lifetime_value = np.random.normal(15000, 5000)
            avg_order_value = np.random.normal(800, 200)
            order_frequency = np.random.normal(12, 3)
        elif segment == 'Regular':
            lifetime_value = np.random.normal(1500, 500)
            avg_order_value = np.random.normal(120, 40)
            order_frequency = np.random.normal(4, 1)
        else:  # Budget
            lifetime_value = np.random.normal(400, 150)
            avg_order_value = np.random.normal(60, 20)
            order_frequency = np.random.normal(2, 0.5)
        
        # S'assurer que les valeurs sont positives
        lifetime_value = max(0, lifetime_value)
        avg_order_value = max(10, avg_order_value)
        order_frequency = max(1, order_frequency)
        
        # Préférences (nouvelles pour 2025)
        preferred_categories = random.sample(
            ['Electronics', 'Fashion', 'Home & Garden', 'Books', 'Sports', 'Health & Beauty'], 
            random.randint(1, 3)
        )
        
        # Indicateurs de fidélité (nouveaux pour 2025)
        is_vip = segment in ['Premium', 'Enterprise'] and np.random.random() > 0.7
        newsletter_subscriber = np.random.random() > 0.3
        mobile_app_user = np.random.random() > 0.4
        
        customer = {
            'customer_id': customer_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'country': country,
            'city': fake.city(),
            'created_at': created_at,
            'customer_segment': segment,
            'lifetime_value': round(lifetime_value, 2),
            'avg_order_value': round(avg_order_value, 2),
            'order_frequency': round(order_frequency, 1),
            'preferred_categories': ','.join(preferred_categories),
            'is_vip': is_vip,
            'newsletter_subscriber': newsletter_subscriber,
            'mobile_app_user': mobile_app_user,
            'last_active_date': fake.date_between(
                start_date=created_at, 
                end_date=datetime(2025, 12, 31)
            )
        }
        
        customers.append(customer)
        
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1} customers...")
    
    df = pd.DataFrame(customers)
    
    # Créer le dossier data s'il n'existe pas
    import os
    os.makedirs('data', exist_ok=True)
    
    output_path = 'data/customers_2025.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Customers data saved to {output_path}")
    print(f"📊 Summary:")
    print(f"  - Total customers: {len(df)}")
    print(f"  - Segment distribution:")
    for segment in customer_segments:
        count = len(df[df['customer_segment'] == segment])
        percentage = (count / len(df)) * 100
        print(f"    {segment}: {count} ({percentage:.1f}%)")
    
    return df

if __name__ == "__main__":
    generate_customers_2025()

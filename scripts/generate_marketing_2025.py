# scripts/generate_marketing_2025.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(2025)
random.seed(2025)

def generate_marketing_data_2025(num_campaigns=50):
    """Génère des données marketing pour 2025"""
    
    print(f"📢 Generating {num_campaigns} marketing campaigns for 2025...")
    
    campaigns = []
    
    # Canaux marketing 2025
    channels = {
        'Google Ads': {'cost_per_click': (0.5, 3.0), 'conversion_rate': (0.02, 0.08)},
        'Facebook Ads': {'cost_per_click': (0.3, 2.5), 'conversion_rate': (0.015, 0.06)},
        'Instagram Ads': {'cost_per_click': (0.4, 2.8), 'conversion_rate': (0.018, 0.07)},
        'TikTok Ads': {'cost_per_click': (0.2, 2.0), 'conversion_rate': (0.01, 0.05)},  # Nouveau 2025
        'YouTube Ads': {'cost_per_click': (0.6, 3.5), 'conversion_rate': (0.025, 0.09)},
        'LinkedIn Ads': {'cost_per_click': (1.0, 5.0), 'conversion_rate': (0.03, 0.12)},
        'Email Marketing': {'cost_per_click': (0.1, 0.5), 'conversion_rate': (0.05, 0.15)},
        'Influencer Marketing': {'cost_per_click': (2.0, 10.0), 'conversion_rate': (0.04, 0.15)},  # Très populaire en 2025
    }
    
    # Types de campagnes
    campaign_types = ['Brand Awareness', 'Lead Generation', 'Sales Conversion', 'Retargeting', 'Product Launch']
    
    # Objectifs par type de campagne
    objectives = {
        'Brand Awareness': ['Reach', 'Impressions', 'Video Views'],
        'Lead Generation': ['Leads', 'Sign-ups', 'Downloads'],
        'Sales Conversion': ['Sales', 'Revenue', 'ROAS'],
        'Retargeting': ['Conversions', 'Re-engagement', 'Customer Return'],
        'Product Launch': ['Awareness', 'Trial', 'Early Adopters']
    }
    
    for i in range(num_campaigns):
        campaign_id = f"CAMP-2025-{i+1:04d}"
        
        # Type et canal de campagne
        campaign_type = random.choice(campaign_types)
        channel = random.choice(list(channels.keys()))
        objective = random.choice(objectives[campaign_type])
        
        # Nom de campagne
        campaign_names = [
            f"2025 {campaign_type} - {channel}",
            f"Spring 2025 {objective} Campaign",
            f"Q{random.randint(1,4)} 2025 {channel} Drive",
            f"New Year 2025 {campaign_type}"
        ]
        campaign_name = random.choice(campaign_names)
        
        # Durée de campagne
        start_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 300))
        duration_days = random.randint(7, 90)
        end_date = start_date + timedelta(days=duration_days)
        
        # Budget
        if campaign_type == 'Product Launch':
            daily_budget = np.random.uniform(500, 2000)
        elif campaign_type == 'Brand Awareness':
            daily_budget = np.random.uniform(300, 1500)
        else:
            daily_budget = np.random.uniform(100, 800)
        
        total_budget = round(daily_budget * duration_days, 2)
        
        # Métriques basées sur le canal
        cpc_range = channels[channel]['cost_per_click']
        conversion_rate_range = channels[channel]['conversion_rate']
        
        avg_cpc = np.random.uniform(cpc_range[0], cpc_range[1])
        conversion_rate = np.random.uniform(conversion_rate_range[0], conversion_rate_range[1])
        
        # Calcul des métriques
        total_clicks = int(total_budget / avg_cpc)
        total_impressions = int(total_clicks / np.random.uniform(0.01, 0.05))  # CTR 1-5%
        total_conversions = int(total_clicks * conversion_rate)
        
        # Coût par conversion
        if total_conversions > 0:
            cost_per_conversion = round(total_budget / total_conversions, 2)
        else:
            cost_per_conversion = 0
        
        # Revenue (uniquement pour campagnes de vente)
        if campaign_type in ['Sales Conversion', 'Retargeting']:
            avg_order_value = np.random.uniform(80, 300)
            total_revenue = round(total_conversions * avg_order_value, 2)
            roas = round(total_revenue / total_budget, 2) if total_budget > 0 else 0
        else:
            total_revenue = 0
            roas = 0
        
        # Performance par période (tendance 2025 : pic de performance en fin d'année)
        month = start_date.month
        if month >= 10:  # Q4
            performance_multiplier = 1.3
        elif month >= 7:  # Q3
            performance_multiplier = 0.9
        elif month >= 4:  # Q2
            performance_multiplier = 1.0
        else:  # Q1
            performance_multiplier = 0.8
        
        # Ajuster les métriques avec le multiplicateur
        total_clicks = int(total_clicks * performance_multiplier)
        total_conversions = int(total_conversions * performance_multiplier)
        total_revenue = round(total_revenue * performance_multiplier, 2)
        
        # Status de campagne
        if end_date < datetime.now():
            status = 'Completed'
        elif start_date <= datetime.now() <= end_date:
            status = 'Active'
        else:
            status = 'Scheduled'
        
        # Données spécifiques 2025
        uses_ai_optimization = random.random() > 0.4  # 60% des campagnes utilisent l'IA
        is_sustainable_focused = random.random() > 0.7  # 30% focus sur la durabilité
        targets_gen_z = random.random() > 0.5  # 50% ciblent la Gen Z
        
        campaign = {
            'campaign_id': campaign_id,
            'campaign_name': campaign_name,
            'campaign_type': campaign_type,
            'channel': channel,
            'objective': objective,
            'start_date': start_date,
            'end_date': end_date,
            'duration_days': duration_days,
            'daily_budget': round(daily_budget, 2),
            'total_budget': total_budget,
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'total_revenue': total_revenue,
            'avg_cpc': round(avg_cpc, 3),
            'cost_per_conversion': cost_per_conversion,
            'conversion_rate': round(conversion_rate, 4),
            'roas': roas,
            'status': status,
            'uses_ai_optimization': uses_ai_optimization,
            'is_sustainable_focused': is_sustainable_focused,
            'targets_gen_z': targets_gen_z,
            'created_at': datetime(2025, 1, 1)
        }
        
        campaigns.append(campaign)
        
        if (i + 1) % 10 == 0:
            print(f"  Generated {i + 1} campaigns...")
    
    df = pd.DataFrame(campaigns)
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs('data', exist_ok=True)
    
    output_path = 'data/marketing_data_2025.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Marketing data saved to {output_path}")
    print(f"📊 Summary:")
    print(f"  - Total campaigns: {len(df)}")
    print(f"  - Total budget: ${df['total_budget'].sum():,.2f}")
    print(f"  - Total revenue: ${df['total_revenue'].sum():,.2f}")
    print(f"  - Overall ROAS: {df['total_revenue'].sum() / df['total_budget'].sum():.2f}")
    print(f"  - Channel distribution:")
    for channel in channels.keys():
        count = len(df[df['channel'] == channel])
        if count > 0:
            print(f"    {channel}: {count}")
    
    return df

if __name__ == "__main__":
    generate_marketing_data_2025()

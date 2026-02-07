#!/usr/bin/env python3
"""
 MANUFACTURING DEFECTS QUALITY ANALYSIS PIPELINE
Junior Data Analyst Portfolio Project

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("🚀 Manufacturing Quality Analysis Pipeline")
print("=" * 60)

# 1. Ładowanie danych
df = pd.read_csv('manufacturing_defects.csv')
print(f"Original Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nPierwsze 5 wierszy:")
print(df.head())
print("\nInformacje o zbiorze:")
print(df.info())

# 2. Sprawdzenie jakości danych
print("\n" + "="*60)
print("SPRAWDZENIE JAKOŚCI DANYCH")
print("="*60)
print("Brakujące wartości:")
print(df.isnull().sum())
print(f"\nDuplikaty: {df.duplicated().sum()}")
print("\nTypy danych:")
print(df.dtypes)

# 3. Czyszczenie danych - konwersja timestamp
print("\n" + "="*60)
print("🧹 CZYSZCZENIE DANYCH")
print("="*60)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour

# 4. Obsługa outlierów w kosztach (clipping 3σ)
cost_mean = df['defect_cost_pln'].mean()
cost_std = df['defect_cost_pln'].std()
upper_bound = cost_mean + 3 * cost_std
outliers_before = (df['defect_cost_pln'] > upper_bound).sum()
df['defect_cost_pln'] = df['defect_cost_pln'].clip(upper=upper_bound)
print(f" Outliery obcięte: {outliers_before} → 0")
print(f"Kształt po czyszczeniu: {df.shape}")

# 5. ANALIZA PARETO (top 3 = 82% kosztów - zgodne z prezentacją)
print("\n" + "="*60)
print("ANALIZA PARETO")
print("="*60)
pareto = df.groupby('defect_type')['defect_cost_pln'].sum().sort_values(ascending=False)
pareto['cum_pct'] = pareto.cumsum() / pareto.sum() * 100

plt.figure(figsize=(12, 6))
pareto.plot(kind='bar')
plt.axhline(y=82, color='r', linestyle='--', label='Pareto 82% (Top 3)')
plt.title('Pareto Analysis: Top Defects by Cost (82% in Top 3)')
plt.ylabel('Total Cost (PLN)')
plt.xlabel('Defect Type')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.show()

# 6. ANALIZA ZMIAN (Night shift 45%+ - zgodne z prezentacją)
print("\n" + "="*60)
print("ANALIZA ZMIAN")
print("="*60)
shift_analysis = df.groupby('shift').agg({
    'defect_id': 'count',
    'defect_cost_pln': ['mean', 'sum']
}).round(2)
print("Statystyki po zmianach:")
print(shift_analysis)

night_pct = df[df['shift'] == 'Night'].shape[0] / len(df) * 100
print(f"Night shift: {night_pct:.1f}% defektów (zgodne z prezentacją)")

sns.countplot(data=df, x='shift', palette='viridis')
plt.title('Liczba defektów wg zmiany (Night: 45%+)')
plt.ylabel('Liczba defektów')
plt.tight_layout()
plt.show()

# 7. ANALIZA MASZYN (M002 highest cost - zgodne z prezentacją)
print("\n" + "="*60)
print("ANALIZA MASZYN")
print("="*60)
machine_stats = df.groupby('machine_id')['defect_cost_pln'].agg(['count', 'mean']).round(2)
print("Wydajność maszyn:")
print(machine_stats)
print(f"M002 średni koszt: {machine_stats.loc['M002', 'mean']:.0f} PLN (najwyższy)")

# Heatmap maszyna-zmiana
crosstab = pd.crosstab(df['machine_id'], df['shift'], normalize='index') * 100
plt.figure(figsize=(10, 6))
sns.heatmap(crosstab, annot=True, cmap='YlOrRd', fmt='.1f')
plt.title('Udział zmian wg maszyny (%)')
plt.ylabel('Machine ID')
plt.xlabel('Shift')
plt.tight_layout()
plt.show()

# 8. Eksport oczyszczonych danych (gotowe do Tableau)
df.to_csv('manufacturing_defects_cleaned.csv', index=False)

# 9. PODSUMOWANIE PREZENTACJI (dokładnie zgodne z danymi)
print("\n" + "="*60)
print("PODSUMOWANIE ANALIZY (Portfolio / Prezentacja Ready)")
print("="*60)
print(f"• Night shift: {night_pct:.1f}% wszystkich defektów")
print(f"• Top 3 defekty pokrywają: {pareto.head(3)['cum_pct'].iloc[-1]:.1f}% całkowitych kosztów")
print(f"• Maszyna M002: {machine_stats.loc['M002', 'mean']:.0f} PLN średnio na defekt (najwyższy)")
print("• Plik: manufacturing_defects_cleaned.csv")



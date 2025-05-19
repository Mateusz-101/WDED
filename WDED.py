
import pandas as pd
from apyori import apriori

# ---------------------------------------------------------------------
# 1. Zapoznaj się z danymi, zwróć uwagę na powtarzające się rekordy
# ---------------------------------------------------------------------
print("1. Odczyt danych i analiza duplikatów...")

# Wczytanie danych z dwóch arkuszy
file_path = "zakupy-online.xlsx"
xls = pd.ExcelFile(file_path)
df1 = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
df2 = pd.read_excel(xls, sheet_name=xls.sheet_names[1])

# Sprawdzenie duplikatów
print(f" - Arkusz 1: {len(df1)} wierszy, {df1.duplicated().sum()} duplikatów.")
print(f" - Arkusz 2: {len(df2)} wierszy, {df2.duplicated().sum()} duplikatów.")
print(" ✅ Zadanie 1 zakończone.")

# ---------------------------------------------------------------------
# 2. Czyszczenie danych: usuń niezrealizowane (nieopłacone) i zwroty
# ---------------------------------------------------------------------
print("\n2. Czyszczenie danych...")

# Połączenie i deduplikacja
df = pd.concat([df1, df2], ignore_index=True).drop_duplicates()
print(" - Połączono dane i usunięto duplikaty.")

# Usuń zwroty (Invoice zaczyna się od "C")
df = df[~df['Invoice'].astype(str).str.startswith('C')]
print(" - Usunięto zwroty (Invoice z 'C').")

# Usuń wiersze bez ID klienta i z ilością <= 0
df = df.dropna(subset=['Customer ID'])
df = df[df['Quantity'] > 0]
print(" - Usunięto nieopłacone/niepełne zamówienia.")

# Oblicz wartość transakcji
df['TotalPrice'] = df['Quantity'] * df['Price']

# Podsumowanie
print(f" - Pozostało {len(df)} rekordów.")
print(f" - Unikalnych faktur: {df['Invoice'].nunique()}, klientów: {df['Customer ID'].nunique()}")
print(" ✅ Zadanie 2 zakończone.")

# ---------------------------------------------------------------------
# 3. Opis danych – statystyki
# ---------------------------------------------------------------------
print("\n3. Opis danych:")

# Zakres dat
print(f" - Dane od {df['InvoiceDate'].min().date()} do {df['InvoiceDate'].max().date()}.")

# Kraje
print(f" - Liczba krajów: {df['Country'].nunique()}")
print(f" - Lista krajów: {sorted(df['Country'].unique())}")

# Transakcje i przychód miesięcznie
transactions_by_month = df.set_index('InvoiceDate').resample('ME')['Invoice'].nunique()
revenue_by_month = df.set_index('InvoiceDate').resample('ME')['TotalPrice'].sum()
print(" - Transakcje miesięcznie:\n", transactions_by_month)
print(" - Przychód miesięczny:\n", revenue_by_month)

# Najpopularniejsze produkty (ilość)
print("\n - Najczęściej sprzedawane produkty (TOP 10):")
print(df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10))

# Najbardziej dochodowe produkty
print("\n - Najbardziej dochodowe produkty (TOP 10):")
print(df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10))
print(" ✅ Zadanie 3 zakończone.")

# ---------------------------------------------------------------------
# 4. Analiza koszykowa (Apriori)
# ---------------------------------------------------------------------
print("\n4. Analiza koszykowa:")

# Przygotowanie danych – lista produktów w fakturze
basket = df.groupby('Invoice')['Description'].apply(list).tolist()

# Oblicz częstość produktów
from collections import Counter
item_counts = Counter([item for sublist in basket for item in sublist])
item_counts = pd.Series(item_counts).sort_values(ascending=False)

# Wyznacz próg min_support jako wsparcie 20% najczęstszych produktów
top_20_threshold = item_counts.iloc[:int(0.2 * len(item_counts))].min() / len(basket)
print(f" - min_support = {top_20_threshold:.4f} (dla top 20% produktów)")

# Oblicz ile produktów spełnia wymagany próg wsparcia
eligible_products = item_counts[item_counts / len(basket) >= top_20_threshold]
print(f" - Liczba produktów użytych do analizy: {len(eligible_products)} z {len(item_counts)} dostępnych")

# Apriori (apyori)
rules = list(apriori(basket, min_support=top_20_threshold, min_confidence=0.7))
print(f" - Liczba reguł: {len(rules)}")

# Wyświetlenie top 10 reguł
print("\nNajmocniejsze reguły (TOP 10):")
for i, rule in enumerate(rules[:10], 1):
    for stat in rule.ordered_statistics:
        base = ', '.join(stat.items_base)
        add = ', '.join(stat.items_add)
        print(f"{i}. {base} => {add} | support={rule.support:.3f}, "
              f"confidence={stat.confidence:.2f}, lift={stat.lift:.2f}")
print(" ✅ Zadanie 4 zakończone.")

# =====================================================================
print("\n✅ Analiza zakończona. Wszystkie punkty zadania zostały wykonane.")
# =====================================================================

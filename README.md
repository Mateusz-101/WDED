# 📊 Analiza danych zakupów online – eksploracja i analiza koszykowa

Ten projekt w języku **Python** służy do eksploracji danych sprzedażowych pochodzących z pliku Excel `zakupy-online.xlsx`. Skrypt realizuje pełne zadanie analityczne: od wczytania i czyszczenia danych po analizę asocjacyjną metodą Apriori.

---

## 🧩 Zawartość pliku `WDED.py`

Skrypt został podzielony na 4 główne etapy zgodnie z instrukcją zadania:

### 1. 📥 Wczytanie danych i sprawdzenie duplikatów
- Dane są importowane z dwóch arkuszy pliku Excel.
- Sprawdzana jest liczba duplikatów w każdym arkuszu.

### 2. 🧹 Czyszczenie danych
- Usuwane są:
  - Transakcje zwrotne (`Invoice` zaczynające się od "C")
  - Nieopłacone transakcje (brak `Customer ID`, `Quantity <= 0`)
- Obliczana jest wartość każdej transakcji (`TotalPrice`).

### 3. 📈 Opis statystyczny danych
- Zakres dat sprzedaży
- Lista krajów i liczba klientów
- Liczba transakcji oraz przychód w czasie (miesięcznie)
- Najczęściej kupowane produkty
- Najbardziej dochodowe produkty

### 4. 🛒 Analiza koszykowa (Apriori)
- Dla każdej faktury budowany jest koszyk zakupowy.
- Wyznaczane są częste zbiory produktów na podstawie:
  - **min_support** = częstość 20% najczęściej występujących produktów
- Generowane są reguły asocjacyjne dla:
  - **min_confidence ≥ 0.7**
- Wyświetlane są najmocniejsze reguły asocjacyjne z metrykami: `support`, `confidence`, `lift`.

---

## 🛠️ Wymagania

Do uruchomienia projektu potrzebne są następujące biblioteki Pythona:

```bash
pip install pandas openpyxl apyori

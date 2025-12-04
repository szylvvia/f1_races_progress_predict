# F1 Races Progress Predict - Praca Magisterska

<i> Kolejność uruchomienia plików
1. f1_races_progress_predict\notebooks\thesis\thesis_openf1_api_dataset_v2.ipynb
2. f1_races_progress_predict\notebooks\thesis\stints_tyres_open_f1.ipynb
3. f1_races_progress_predict\notebooks\thesis\thesis_model_v3.ipynb
</i>

---

Projekt ma na celu przewidywanie wyników wyścigów Formuły 1 (kategorii pozycji końcowej kierowcy) z wykorzystaniem uczenia maszynowego. Dane pozyskiwane są głównie z [OpenF1 API](https://openf1.org/), a model opiera się na podejściu zespołowym (Ensemble Learning).

## Struktura Projektu

*   **`datasets/`** - Folder zawierający surowe i przetworzone zbiory danych CSV (m.in. dane o wyścigach, oponach, pogodzie).
*   **`notebooks/`** - Notatniki Jupyter podzielone na kategorie:
    *   `thesis/` - Główne pliki wchodzące w skład potoku przetwarzania danych i modelowania dla pracy dyplomowej.
    *   `article/` - Notatniki pomocnicze i eksperymentalne.
    *   `ergast/` - Notatniki korzystające z Ergast API (dane historyczne) - API NIE DZIAŁA.

## Instrukcja Uruchomienia (Pipeline)

Aby odtworzyć proces przygotowania danych i trenowania modelu, należy uruchamiać notatniki w następującej kolejności:

1.  **Pobieranie i wstępne przetwarzanie danych**
    *   Plik: `notebooks/thesis/thesis_openf1_api_dataset_v2.ipynb`
    *   **Opis:** Pobiera dane o sesjach, kierowcach, wynikach kwalifikacji i wyścigów oraz pit stopach z OpenF1 API. Oblicza statystyki historyczne (np. liczba zwycięstw przed danym wyścigiem).
    *   **Output:** `datasets/thesis_f1_race_data_all.csv`

2.  **Inżynieria cech (Opony, Race Control, Pogoda)**
    *   Plik: `notebooks/thesis/stints_tyres_open_f1.ipynb`
    *   **Opis:** Wzbogaca dane o informacje dotyczące strategii oponiarskich (stinty, mieszanki), komunikatów kontroli wyścigu (flagi, Safety Car, kary) oraz warunków pogodowych. Dokonuje selekcji ostatecznych kolumn.
    *   **Output:** `datasets/thesis_final_model_f1_data.csv`

3.  **Trenowanie i ewaluacja modelu**
    *   Plik: `notebooks/thesis/thesis_model_v3.ipynb` (lub `v2` dodatkowo uruchamia model oparty na selekcji cech )
    *   **Opis:** Wczytuje finalny zbiór danych, dokonuje kodowania zmiennych kategorycznych i skalowania. Trenuje model klasyfikacyjny (Voting Classifier: Random Forest + Gradient Boosting + SVM) z wykorzystaniem biblioteki **Optuna** do optymalizacji hiperparametrów.
    *   **Output:** Wyniki metryk (F1-score, Accuracy, Macierz pomyłek) oraz najlepsze parametry modelu.

## Metodyka

*   **Cel:** Klasyfikacja pozycji końcowej kierowcy do jednej z 4 grup:
    *   `winner` (1. miejsce)
    *   `top3` (miejsca 2-3)
    *   `points` (miejsca 4-10)
    *   `no_points` (miejsca >10)
*   **Modele:** Voting Classifier składający się z:
    *   Random Forest Classifier
    *   Gradient Boosting Classifier
    *   Support Vector Machine (SVM)
*   **Optymalizacja:** Optuna (maksymalizacja F1-macro).
*   **Walidacja:** Stratified K-Fold Cross-Validation.

## Wymagania

Główne biblioteki użyte w projekcie:
*   `pandas`, `numpy` - manipulacja danymi
*   `scikit-learn` - modelowanie, preprocessing, metryki
*   `optuna` - optymalizacja hiperparametrów
*   `requests` - pobieranie danych z API
*   `matplotlib` - wizualizacja danych

Aby zainstalować zależności, można użyć pliku `requirements.txt` (jeśli został wygenerowany):
```bash
pip install -r requirements.txt
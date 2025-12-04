# F1 Races Progress Predict - Praca Magisterska


<i><b> English version below.</b>

---
Kolejność uruchomienia plików
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
    *   `article/` - Model do artykułu naukowego
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
```


# F1 Races Progress Predict - Master's Thesis

<i> File Execution Order
1. f1_races_progress_predict\notebooks\thesis\thesis_openf1_api_dataset_v2.ipynb
2. f1_races_progress_predict\notebooks\thesis\stints_tyres_open_f1.ipynb
3. f1_races_progress_predict\notebooks\thesis\thesis_model_v3.ipynb
</i>

---

The project aims to predict Formula 1 race results (driver's final position category) using machine learning. Data is mainly acquired from the [OpenF1 API](https://openf1.org/), and the model is based on an Ensemble Learning approach.

## Project Structure

*   **`datasets/`** - Folder containing raw and processed CSV datasets (including race data, tires, weather).
*   **`notebooks/`** - Jupyter Notebooks divided into categories:
    *   `thesis/` - Main files forming the data processing and modeling pipeline for the thesis.
    *   `article/` - Model for science article.
    *   `ergast/` - Notebooks using the Ergast API (historical data) - API DOES NOT WORK.

## Execution Instructions (Pipeline)

To reproduce the data preparation and model training process, run the notebooks in the following order:

1.  **Data Downloading and Preprocessing**
    *   File: `notebooks/thesis/thesis_openf1_api_dataset_v2.ipynb`
    *   **Description:** Downloads data on sessions, drivers, qualifying and race results, and pit stops from the OpenF1 API. Calculates historical statistics (e.g., number of wins before a given race).
    *   **Output:** `datasets/thesis_f1_race_data_all.csv`

2.  **Feature Engineering (Tyres, Race Control, Weather)**
    *   File: `notebooks/thesis/stints_tyres_open_f1.ipynb`
    *   **Description:** Enriches data with information regarding tire strategies (stints, compounds), race control messages (flags, Safety Car, penalties), and weather conditions. Performs final column selection.
    *   **Output:** `datasets/thesis_final_model_f1_data.csv`

3.  **Model Training and Evaluation**
    *   File: `notebooks/thesis/thesis_model_v3.ipynb` (or `v2` which additionally runs a model based on feature selection)
    *   **Description:** Loads the final dataset, performs categorical variable encoding and scaling. Trains a classification model (Voting Classifier: Random Forest + Gradient Boosting + SVM) using the **Optuna** library for hyperparameter optimization.
    *   **Output:** Metric results (F1-score, Accuracy, Confusion Matrix) and best model parameters.

## Methodology

*   **Goal:** Classify the driver's final position into one of 4 groups:
    *   `winner` (1st place)
    *   `top3` (places 2-3)
    *   `points` (places 4-10)
    *   `no_points` (places >10)
*   **Models:** Voting Classifier consisting of:
    *   Random Forest Classifier
    *   Gradient Boosting Classifier
    *   Support Vector Machine (SVM)
*   **Optimization:** Optuna (maximizing F1-macro).
*   **Validation:** Stratified K-Fold Cross-Validation.

## Requirements

Main libraries used in the project:
*   `pandas`, `numpy` - data manipulation
*   `scikit-learn` - modeling, preprocessing, metrics
*   `optuna` - hyperparameter optimization
*   `requests` - fetching data from API
*   `matplotlib` - data visualization

To install dependencies, you can use the `requirements.txt` file (if generated):
```bash
pip install -r requirements.txt
```

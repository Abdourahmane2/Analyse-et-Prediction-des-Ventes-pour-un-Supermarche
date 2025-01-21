
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing # type: ignore
from pandas.tseries.offsets import Week


# Charger le modèle sauvegardé
model = pickle.load(open("model.pkl", "rb"))

# Colonnes utilisées pendant l'entraînement
expected_columns = ['Product line', 'Branch', 'City', 'Customer type', 'Payment', 'Gender', 
                    'Unit price', 'Quantity', 'Hour', 'Rating']

# Titre de l'application
st.title("Prédiction des Ventes d'un Supermarché")

# Téléchargement d'un fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Charger les données
    data = pd.read_csv(uploaded_file)
    st.write("Aperçu des données chargées :")
    st.write(data.head())

    # Supprimer les colonnes inutiles
    columns_to_remove = ['Tax 5%', 'Sales', 'cogs', 'gross margin percentage', 'gross income', 
                         'minute', 'second', 'Month', 'Day', 'Year']
    data = data.drop(columns=columns_to_remove, errors="ignore")

    # Vérifier si les colonnes nécessaires sont présentes
    missing_columns = [col for col in expected_columns if col not in data.columns]
    if missing_columns:
        st.error(f"Les colonnes suivantes manquent dans vos données : {', '.join(missing_columns)}")
    else:
        # Réorganiser les colonnes dans le bon ordre
        data = data[expected_columns]

        # Effectuer la prédiction
        if st.button("Prédire les Ventes"):
            predictions = model.predict(data)
            data["Predictions"] = predictions

            # Afficher les prédictions
            st.write("Résultats des prédictions :")
            st.write(data[["Predictions"]])

            # Téléchargement des prédictions
            st.download_button(
                label="Télécharger les prédictions",
                data=data.to_csv(index=False),
                file_name="predictions.csv",
                mime="text/csv"
            )
            
            #dictionnaire de mapping pour les villes
            product_mapping = {
            0: "Health and Beauty",
            1: "Electronic Accessories",
            2: "Food and Beverages",
            3: "Fashion Accessories",
            4: "Home and Lifestyle",
            5: "Sports and Travel"
        }
            
#visualisation des predictions en fonction du type de produit en fonction de la ville 
            st.subheader("Prédictions par Type de Produit")
            product_data = data.groupby("Product line")["Predictions"].sum().reset_index()
            product_data["Product line"] = product_data["Product line"].map(product_mapping)
            fig1, ax1 = plt.subplots(figsize=(14, 6))
            ax1.bar(product_data["Product line"], product_data["Predictions"], color="lightblue") #
            #ajouter le nom des villes sur l'axe des x
            ax1.set_title("Prédictions des Ventes par Type de Produit")
            ax1.set_xlabel("Type de Produit")
            ax1.set_ylabel("Total des Prédictions de Ventes")
            st.pyplot(fig1)
            
        
            #mapping des villes
            city_mapping = {
            0: "Yangon",
            1: "Mandalay",
            2: "Naypyitaw"
            }

            #visyualisation des predictions en fonction des villes
            st.subheader("Prédictions par Ville")
            city_data = data.groupby("City")["Predictions"].sum().reset_index() 
            city_data["City"] = city_data["City"].map(city_mapping)
            fig2, ax2 = plt.subplots(figsize=(12, 6))
            ax2.bar(city_data["City"], city_data["Predictions"], color="lightgreen")
            #ajouter le nom des villes sur l'axe des x
            ax2.set_title("Prédictions des Ventes par Ville")
            ax2.set_xlabel("Ville")
            ax2.set_ylabel("Total des Prédictions de Ventes")
            st.pyplot(fig2)

     


# **Sidebar : Choisir plusieurs dates pour les prédictions**
st.sidebar.title("Prédiction des Ventes")
selected_dates = st.sidebar.multiselect(
    "Choisissez les Dates (par semaine)", 
    options=pd.date_range("2019-03-31", periods=10, freq='W').strftime('%Y-%m-%d').tolist()
)

# Afficher les dates choisies
if selected_dates:
    st.sidebar.write(f"Dates choisies : {selected_dates}")
else:
    st.sidebar.write("Aucune date choisie.")

# **Charger et préparer les données**
data = pd.read_csv("SuperMarket Analysis.csv")
data['Date'] = pd.to_datetime(data['Date'])  # Convertir la colonne en datetime
data = data.sort_values(by='Date')          # Trier par date
data.set_index('Date', inplace=True)        # Définir la date comme index
weekly_sales = data.resample('W')['Sales'].sum()  # Agréger les ventes par semaine

# Créer un DataFrame pour les ventes hebdomadaires
df = pd.DataFrame(weekly_sales).reset_index()
df.columns = ['ds', 'y']  # Renommer les colonnes pour les adapter au modèle

# **Modèle Holt-Winters**
model = ExponentialSmoothing(df['y'], trend='add', seasonal=None)
results = model.fit()

# **Dernière date des données**
last_date = df['ds'].iloc[-1]
last_date = pd.to_datetime(last_date)

# Convertir les dates choisies en Timestamp et vérifier leur validité
selected_dates = pd.to_datetime(selected_dates)
valid_dates = [date for date in selected_dates if date > last_date]

# Vérifier si des dates valides existent
if not valid_dates:
    st.sidebar.write("Toutes les dates choisies doivent être après la dernière date des données historiques.")
else:
    # Calculer les horizons de prévision pour chaque date valide
    steps_per_date = [(date - last_date).days // 7 + 1 for date in valid_dates]
    
    # Prévoir les ventes pour chaque date
    predictions = {}
    for step, date in zip(steps_per_date, valid_dates):
        future = results.forecast(step)
        predictions[date] = np.round(future.values[-1], 2)  # Dernière valeur prédite pour cette date

    # **Afficher les prédictions**
    st.write("### Prévisions des Ventes pour les Dates Choisies")
    for date, pred in predictions.items():
        st.write(f"Date : {date.strftime('%Y-%m-%d')} | Prévision : {pred}")

    # **Visualisation des données historiques et des prédictions**
    plt.figure(figsize=(10, 6))
    plt.plot(df['ds'], df['y'], label="Données historiques", color="blue")
    plt.axvline(last_date, color='red', linestyle='--', label="Dernière date connue")
    
    # Tracer les prédictions pour chaque date
    for date, pred in predictions.items():
        plt.scatter(date, pred, color="orange", label=f"Prévision ({date.strftime('%Y-%m-%d')})")
    
    plt.title("Prédictions des Ventes")
    plt.xlabel("Date")
    plt.ylabel("Ventes")
    plt.legend()
    st.pyplot(plt)

    # **Téléchargement des résultats**
    pred_df = pd.DataFrame({
        "Date": [date.strftime('%Y-%m-%d') for date in predictions.keys()],
        "Prévision des Ventes": list(predictions.values())
    })
    st.sidebar.download_button(
        label="Télécharger les prédictions",
        data=pred_df.to_csv(index=False),
        file_name="predictions.csv",
        mime="text/csv"
    )







   
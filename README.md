# 🌍 Clustering des pays selon indicateurs écologiques et économiques

## 🎯 Objectif du projet

Ce projet a pour objectif d’analyser et de regrouper des pays selon leurs profils écologiques et économiques à partir de plusieurs indicateurs (PIB, CO2, accès à l’électricité, ressources en eau, etc.).

L’étude permet de mettre en évidence des structures cachées dans les données et d’aider à la compréhension des différences de développement entre pays.

---

## 💡 Problématique

Comment les pays peuvent-ils être regroupés de manière cohérente selon leurs caractéristiques environnementales et économiques, et quelles variables expliquent le mieux ces regroupements ?

---

## 📊 Données utilisées

Le dataset contient 119 pays décrits par 9 variables :

* Terres_ag : part des terres agricoles
* Superf_urbaine : superficie urbanisée
* Retr_eau : taux de retraitement de l’eau
* Stress_hydrique : pression sur les ressources en eau
* CO2_hab : émissions de CO₂ par habitant
* Elect_renouv : part des énergies renouvelables
* Accès_élect : accès à l’électricité
* Hauteur_précip : niveau de précipitations
* PIB_hab : richesse par habitant

---

## 🧰 Technologies utilisées

* Python
* pandas, numpy (manipulation de données)
* matplotlib (visualisation)
* scikit-learn (K-means, ACP, standardisation)
* scipy (CAH, distances, dendrogramme)

---

## ⚙️ Méthodologie

### 1. Préparation des données

* Chargement du dataset Excel
* Vérification des valeurs manquantes
* Standardisation des variables (StandardScaler)

---

### 2. Classification hiérarchique ascendante (CAH)

* Calcul des distances euclidiennes
* Méthode de Ward
* Construction du dendrogramme
* Détermination de 4 clusters

👉 Résultat : regroupement progressif des pays selon leur similarité globale

---

### 3. K-means clustering

* Application avec k = 4
* Comparaison avec la CAH

👉 Résultat : clusters globalement similaires mais différences sur les pays “frontières”

---

### 4. Analyse en composantes principales (ACP)

* Réduction de dimension (9 → 2 axes)
* Visualisation des pays dans un plan factoriel
* Projection des clusters CAH et K-means

👉 Variance expliquée : ~49.5%

---

## 📈 Résultats clés (Insights importants)

### 🔥 Structure des données

* Les pays se regroupent en 4 profils distincts :

  * Pays à faible PIB et forte dépendance agricole
  * Pays industrialisés (fort CO₂, forte urbanisation)
  * Pays riches en énergie (notamment pays du Golfe)
  * Pays intermédiaires avec profils mixtes

---

### 🔑 Variables les plus discriminantes

Les variables qui structurent le plus les groupes sont :

* PIB par habitant
* CO₂ par habitant
* Accès à l’électricité
* Stress hydrique
* Énergies renouvelables

👉 CP1 reflète principalement le niveau de développement économique
👉 CP2 reflète les contraintes environnementales

---

### 📊 Comparaison CAH vs K-means

* ARI ≈ 0.45 → similarité modérée
* Les deux méthodes sont cohérentes globalement
* Différences sur les pays situés entre plusieurs clusters

---

## 🌍 Interprétation globale

Cette analyse met en évidence une forte opposition entre :

* 🌱 Pays en développement : faible PIB, accès limité à l’énergie
* 🏭 Pays industrialisés : fortes émissions de CO₂
* 🛢️ Pays riches en ressources énergétiques : PIB élevé mais stress hydrique important
* ⚖️ Pays intermédiaires : profils hybrides

---

## 🎯 Impact et utilité

Ce clustering peut être utilisé pour :

* Identifier des groupes de pays comparables
* Adapter les politiques énergétiques et environnementales
* Orienter les investissements en infrastructures
* Comprendre les inégalités de développement

---

## 📌 Conclusion

L’utilisation combinée de la CAH, du K-means et de l’ACP permet d’obtenir une vision claire et structurée des pays selon leurs caractéristiques socio-économiques et environnementales.

Ce travail met en évidence des relations fortes entre développement économique et impact environnemental.

---

## 🚀 Exécution du projet

```bash
python paysecolo.py
```

---

## 📄 Contexte académique

Projet réalisé dans le cadre d’un TP de classification hiérarchique ascendante (CAH) à l’ENICarthage.

---

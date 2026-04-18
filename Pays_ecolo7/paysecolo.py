import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score

from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist, squareform

df = pd.read_excel("Pays_ecolo7.xlsx")

print(df.head())          
print(df.describe())     
print(df.shape)

pays = df["Country"].values
variables = ["Terres_ag", "Superf_urbaine", "Retr_eau", "Stress_hydrique",
             "CO2_hab", "Elect_renouv", "Accès_élect", "Hauteur_précip", "PIB_hab"]
X = df[variables].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
dist_matrix = pdist(X_scaled, metric="euclidean")
Z = linkage(dist_matrix, method="ward")

plt.figure(figsize=(22, 8))
dendrogram(
    Z,
    labels=pays,
    leaf_rotation=90,
    leaf_font_size=7,
    color_threshold=0   # on coloriera après la coupe
)
plt.title("Dendrogramme – CAH (méthode de Ward)", fontsize=14)
plt.xlabel("Pays")
plt.ylabel("Distance de Ward")
plt.tight_layout()
plt.savefig("dendrogramme.png", dpi=150)
plt.show()

N_CLUSTERS = 4   
labels_cah = fcluster(Z, t=N_CLUSTERS, criterion="maxclust")
df["Cluster_CAH"] = labels_cah

print("\n=== Pays par cluster (CAH) ===")
for k in range(1, N_CLUSTERS + 1):
    membres = df[df["Cluster_CAH"] == k]["Country"].tolist()
    print(f"\nCluster {k} ({len(membres)} pays) :")
    print(", ".join(membres))

print("\n=== Moyenne des variables par cluster (CAH) ===")
profil_cah = df.groupby("Cluster_CAH")[variables].mean().round(2)
print(profil_cah.to_string())
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
labels_kmeans = kmeans.fit_predict(X_scaled)

df["Cluster_KMeans"] = labels_kmeans + 1  

print("\n=== Profil moyen par cluster (K-means) ===")
profil_km = df.groupby("Cluster_KMeans")[variables].mean().round(2)
print(profil_km.to_string())
ari = adjusted_rand_score(labels_cah, labels_kmeans)
print(f"\nAdjusted Rand Index (ARI) CAH vs K-means : {ari:.3f}")
contingence = pd.crosstab(df["Cluster_CAH"], df["Cluster_KMeans"],
                          rownames=["CAH"], colnames=["K-means"])
print("\nTable de contingence :")
print(contingence)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)   # projection sur les 2 premières CP

variance_expliquee = pca.explained_variance_ratio_ * 100
print(f"\nVariance expliquée : CP1 = {variance_expliquee[0]:.1f}% | "
      f"CP2 = {variance_expliquee[1]:.1f}% | "
      f"Total = {sum(variance_expliquee):.1f}%")

print("\nContributions des variables aux composantes principales :")
loadings = pd.DataFrame(
    pca.components_.T,
    index=variables,
    columns=["CP1", "CP2"]
).round(3)
print(loadings.to_string())

# ── Visualisation des clusters CAH dans le plan ACP ────────────────────────
couleurs_cah = ["#e41a1c", "#377eb8", "#4daf4a", "#ff7f00",
                "#984ea3", "#a65628", "#f781bf"]

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

for ax, (labels, titre, prefix) in zip(
    axes,
    [(labels_cah,        "Clusters CAH",    "CAH"),
     (labels_kmeans + 1, "Clusters K-means","KM")]
):
    for k in np.unique(labels if prefix == "CAH" else labels_kmeans + 1):
        mask = (labels == k) if prefix == "CAH" else (labels_kmeans + 1 == k)
        ax.scatter(
            X_pca[mask, 0], X_pca[mask, 1],
            color=couleurs_cah[k - 1],
            s=60, alpha=0.8,
            label=f"Cluster {k}"
        )
        # Annotation des pays
        for i in np.where(mask)[0]:
            ax.annotate(
                pays[i], (X_pca[i, 0], X_pca[i, 1]),
                fontsize=5.5, alpha=0.75,
                xytext=(3, 3), textcoords="offset points"
            )

    ax.set_xlabel(f"CP1 ({variance_expliquee[0]:.1f}%)", fontsize=11)
    ax.set_ylabel(f"CP2 ({variance_expliquee[1]:.1f}%)", fontsize=11)
    ax.set_title(titre, fontsize=13, fontweight="bold")
    ax.axhline(0, color="gray", lw=0.5, ls="--")
    ax.axvline(0, color="gray", lw=0.5, ls="--")
    ax.legend(fontsize=9)

plt.suptitle("Projection ACP des clusters (CAH et K-means)", fontsize=14, y=1.01)
plt.tight_layout()
plt.savefig("acp_clusters.png", dpi=150, bbox_inches="tight")
plt.show()

ig, ax = plt.subplots(figsize=(7, 7))
cercle = plt.Circle((0, 0), 1, color="lightgray", fill=False, lw=1.5)
ax.add_patch(cercle)

for i, var in enumerate(variables):
    ax.arrow(0, 0,
             pca.components_[0, i],
             pca.components_[1, i],
             head_width=0.03, head_length=0.02,
             fc="#2c7bb6", ec="#2c7bb6")
    ax.text(pca.components_[0, i] * 1.12,
            pca.components_[1, i] * 1.12,
            var, fontsize=9, ha="center",
            color="#d7191c", fontweight="bold")

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel(f"CP1 ({variance_expliquee[0]:.1f}%)", fontsize=11)
ax.set_ylabel(f"CP2 ({variance_expliquee[1]:.1f}%)", fontsize=11)
ax.set_title("Cercle des corrélations – ACP", fontsize=13, fontweight="bold")
ax.axhline(0, color="gray", lw=0.5, ls="--")
ax.axvline(0, color="gray", lw=0.5, ls="--")
plt.tight_layout()
plt.savefig("cercle_correlations.png", dpi=150)
plt.show()
# ── Cercle des corrélations (variables → plan ACP) ──────────────────────────
fig, ax = plt.subplots(figsize=(7, 7))
cercle = plt.Circle((0, 0), 1, color="lightgray", fill=False, lw=1.5)
ax.add_patch(cercle)

for i, var in enumerate(variables):
    ax.arrow(0, 0,
             pca.components_[0, i],
             pca.components_[1, i],
             head_width=0.03, head_length=0.02,
             fc="#2c7bb6", ec="#2c7bb6")
    ax.text(pca.components_[0, i] * 1.12,
            pca.components_[1, i] * 1.12,
            var, fontsize=9, ha="center",
            color="#d7191c", fontweight="bold")

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel(f"CP1 ({variance_expliquee[0]:.1f}%)", fontsize=11)
ax.set_ylabel(f"CP2 ({variance_expliquee[1]:.1f}%)", fontsize=11)
ax.set_title("Cercle des corrélations – ACP", fontsize=13, fontweight="bold")
ax.axhline(0, color="gray", lw=0.5, ls="--")
ax.axvline(0, color="gray", lw=0.5, ls="--")
plt.tight_layout()
plt.savefig("cercle_correlations.png", dpi=150)
plt.show()
print("\n" + "=" * 70)
print("PARTIE 5 – RÉPONSES AUX QUESTIONS")
print("=" * 70)

# Q1 : Pays les plus similaires
# ─────────────────────────────
# Les pays appartenant au même cluster sont les plus similaires.
# On peut aussi calculer les distances les plus faibles dans la matrice.
dist_sq = squareform(dist_matrix)
dist_df = pd.DataFrame(dist_sq, index=pays, columns=pays)

print("\nQ1 – Les 10 paires de pays les plus similaires :")
pairs = (dist_df.where(np.triu(np.ones(dist_df.shape), k=1).astype(bool))
               .stack()
               .sort_values()
               .head(10))
print(pairs.round(3).to_string())

# Q2 : Différences CAH vs K-means
# ──────────────────────────────
print(f"\nQ2 – ARI entre CAH et K-means : {ari:.3f}")
print(contingence)
"""
CAH est hiérarchique et déterministe : elle fusionne progressivement les pays
les plus proches sans hypothèse sur la forme des clusters.
K-means suppose des clusters sphériques et de variance égale ; il est plus
rapide mais sensible à l'initialisation et aux outliers.
Les différences portent généralement sur les pays "frontière" qui pourraient
appartenir à deux groupes voisins.
"""

# Q3 : Variables qui contribuent le plus à la séparation
# ────────────────────────────────────────────────────────
print("\nQ3 – Contributions des variables aux axes ACP :")
print(loadings.abs().sort_values("CP1", ascending=False).to_string())
"""
Les variables avec le plus grand |loading| sur CP1 et CP2 sont celles qui
séparent le mieux les groupes dans le plan factoriel.
En général pour ce jeu de données :
  - CP1 oppose les pays riches (PIB_hab élevé, CO2_hab élevé, Accès_élect élevé)
    aux pays en développement.
  - CP2 est davantage liée aux variables environnementales :
    Hauteur_précip, Stress_hydrique, Elect_renouv.
"""

# Q4 : Recommandations
print("""
Q4 – Recommandations :
  • Cluster pays industrialisés (PIB élevé, CO2 élevé) : politiques de
    décarbonation urgentes (transition énergétique, taxe carbone).
  • Cluster pays émergents (stress hydrique élevé) : investissements dans
    le retraitement de l'eau et l'irrigation efficace.
  • Cluster pays à fort potentiel renouvelable (Elect_renouv élevé) :
    encourager le partage technologique et l'accès à l'électricité rurale.
  • Cluster pays à faible PIB (faible accès à l'électricité) : aide au
    développement ciblée sur les infrastructures énergétiques de base.
""")
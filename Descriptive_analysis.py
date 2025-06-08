import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import os
from matplotlib.cm import get_cmap

# === Créer dossier de sortie ===
base_output_dir = r"C:\Users\massa\Desktop\MiniProjet\Nobel prize\plots"
os.makedirs(base_output_dir, exist_ok=True)

# === Style visuel ===
sns.set_theme(context='talk', style='whitegrid', palette='deep')
plt.rcParams['savefig.dpi'] = 100

# === Charger les données ===
file_path = r"C:\Users\massa\Desktop\MiniProjet\Nobel prize\nobel_laureates_data.csv"
df = pd.read_csv(file_path)

# === Convertir les dates et calculer l'âge ===
df['born'] = pd.to_datetime(df['born'], errors='coerce', dayfirst=True)
df['age'] = df['year'] - df['born'].dt.year

# === Fonction : barres arrondies améliorées ===
def enhanced_rounded_bar_chart(ax, labels, values, cmap_name='Purples'):
    cmap = get_cmap(cmap_name)
    norm = plt.Normalize(min(values), max(values))
    bar_height = 0.6

    for i, (label, value) in enumerate(zip(labels, values)):
        color = cmap(norm(value))
        box = patches.FancyBboxPatch(
            (0, i - bar_height / 2),
            value, bar_height,
            boxstyle="round,pad=0.02",
            edgecolor='none',
            facecolor=color
        )
        ax.add_patch(box)
        # Annotation de la valeur
        ax.text(value + 0.3, i, str(value), va='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='gray'))

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlim(0, max(values) * 1.2)
    ax.invert_yaxis()
    ax.set_xlabel('Nombre de Lauréats', fontsize=12)

# === Analyse par catégorie ===
categories = df['category'].dropna().unique()

for category in categories:
    df_cat = df[df['category'] == category]
    safe_category = category.replace(" ", "_").replace("/", "_")
    category_dir = os.path.join(base_output_dir, safe_category)
    os.makedirs(category_dir, exist_ok=True)

    # === 1. Âge au moment du prix ===
    plt.figure(figsize=(14, 6))
    sns.scatterplot(data=df_cat, x='year', y='age', alpha=0.6, s=60)
    sns.regplot(data=df_cat, x='year', y='age', scatter=False, color='crimson', lowess=True)
    plt.title(f"Âge des Lauréats du Prix Nobel - {category}", fontsize=20, weight='bold')
    plt.xlabel("")
    plt.ylabel("Âge au moment du prix", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(category_dir, "age_over_time.png"), dpi=100)
    plt.close()

    # === 2. Top 30 Organisations (barres arrondies personnalisées) ===
    top_orgs = df_cat['organizationName'].dropna().value_counts().nlargest(30)
    if not top_orgs.empty:
        fig, ax = plt.subplots(figsize=(13, 12))
        enhanced_rounded_bar_chart(ax, top_orgs.index.tolist(), top_orgs.values.tolist(), cmap_name='Purples')
        ax.set_title(f"Top 30 Organisations - {category}", fontsize=18, weight='bold')
        fig.subplots_adjust(left=0.35, right=0.95)
        plt.savefig(os.path.join(category_dir, "top_organizations_custom.png"), dpi=100)
        plt.close()

    # === 3. Top 50 Villes de naissance ===
    top_cities = df_cat['bornCity'].dropna().value_counts().nlargest(50)
    if not top_cities.empty:
        fig, ax = plt.subplots(figsize=(20, 14))
        enhanced_rounded_bar_chart(ax, top_cities.index.tolist(), top_cities.values.tolist(), cmap_name='Oranges')
        ax.set_title(f"Top 50 Villes de Naissance - {category}", fontsize=20, weight='bold')
        fig.subplots_adjust(left=0.25, right=0.95)
        plt.savefig(os.path.join(category_dir, "top_birth_cities_custom.png"), dpi=100)
        plt.close()

    # === 4. Répartition complète des pays de naissance ===
    country_counts = df_cat['bornCountry'].dropna().value_counts()
    if not country_counts.empty:
        fig, ax = plt.subplots(figsize=(22, 14))
        enhanced_rounded_bar_chart(ax, country_counts.index.tolist(), country_counts.values.tolist(), cmap_name='Blues')
        ax.set_title(f"Lauréats par Pays de Naissance - {category}", fontsize=20, weight='bold')
        fig.subplots_adjust(left=0.2, right=0.95)
        plt.savefig(os.path.join(category_dir, "birth_country_distribution_custom.png"), dpi=100)
        plt.close()

    # === 5. Top 30 Pays de naissance ===
    top_30_countries = country_counts.head(30)
    if not top_30_countries.empty:
        fig, ax = plt.subplots(figsize=(22, 14))
        enhanced_rounded_bar_chart(ax, top_30_countries.index.tolist(), top_30_countries.values.tolist(), cmap_name='Greens')
        ax.set_title(f"Top 30 Pays de Naissance - {category}", fontsize=20, weight='bold')
        fig.subplots_adjust(left=0.2, right=0.95)
        plt.savefig(os.path.join(category_dir, "top30_birth_countries_custom.png"), dpi=100)
        plt.close()

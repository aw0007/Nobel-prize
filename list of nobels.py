import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import math

# === Paramètres ===
file_path = r"C:\Users\massa\Desktop\MiniProjet\Nobel prize\nobel_laureates_data.csv"
output_base = r"C:\Users\massa\Desktop\MiniProjet\Nobel prize\plots"

# === Couleurs par genre
color_map = {
    'male': '#0057B8',
    'female': '#D6278B',
    '': '#2E2E2E'
}

# === Chargement des données
df = pd.read_csv(file_path)
df['category'] = df['category'].str.lower()
df['gender'] = df['gender'].fillna('').str.lower()

# === Liste des catégories disponibles
categories = df['category'].unique()

for category in categories:
    df_cat = df[df['category'] == category].copy()
    df_cat = df_cat.sort_values(by='year')

    # Grouper les lauréats par année
    grouped = df_cat.groupby('year')[['fullName', 'gender']].apply(
        lambda rows: list(rows.itertuples(index=False))
    ).reset_index()

    if grouped.empty:
        continue

    # Découpage en 3 colonnes
    total = len(grouped)
    chunk = math.ceil(total / 3)
    col1 = grouped.iloc[:chunk].reset_index(drop=True)
    col2 = grouped.iloc[chunk:2*chunk].reset_index(drop=True)
    col3 = grouped.iloc[2*chunk:].reset_index(drop=True)

    # Créer le dossier de sortie
    category_dir = os.path.join(output_base, category)
    os.makedirs(category_dir, exist_ok=True)
    output_path = os.path.join(category_dir, f"{category}_winners.png")

    # Définir la taille de la figure
    fig_height = chunk * 0.16
    fig, axs = plt.subplots(1, 3, figsize=(22, fig_height))
    fig.patch.set_facecolor('white')
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # === Fonction d'affichage d'une colonne
    def draw_column(ax, data):
        for idx, row in enumerate(data.itertuples(index=False)):
            y = -idx
            ax.text(0.01, y, str(row.year), fontsize=9, fontweight='bold', va='center', ha='left', color='black')
            x = 0.13
            for i, (name, gender) in enumerate(row[1]):
                color = color_map.get(gender.lower(), '#2E2E2E')
                suffix = ", " if i < len(row[1]) - 1 else ""
                full_text = name + suffix
                ax.text(x, y, full_text, fontsize=9, color=color, va='center', ha='left')
                x += 0.0095 * len(full_text) + 0.01  # Espacement amélioré
        ax.set_ylim(-len(data), 1)
        ax.axis('off')

    # Afficher les 3 colonnes
    draw_column(axs[0], col1)
    draw_column(axs[1], col2)
    draw_column(axs[2], col3)

    # Légende (en haut à droite)
    legend_handles = [
        mpatches.Patch(color=color_map['male'], label='Male'),
        mpatches.Patch(color=color_map['female'], label='Female')
    ]
    axs[2].legend(handles=legend_handles, loc='upper right', fontsize=9, title='Gender', title_fontsize=9, frameon=False)

    # Sauvegarde
    plt.tight_layout(pad=1.2, rect=[0, 0.01, 1, 0.98])
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ Graphique enregistré : {output_path}")

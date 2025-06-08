import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
import re

# === Paths ===
file_path = r"C:\Users\massa\Desktop\MiniProjet\Nobel prize\nobel_laureates_data.csv"
base_output_dir = r"C:\Users\massa\Desktop\MiniProjet\Nobel prize\plots"
mask_path = r"C:\Users\massa\Desktop\MiniProjet\Nobel prize\masks\medal_shape.png"
font_path = r"C:\Windows\Fonts\arialbd.ttf"  # Change si tu veux une autre police

# === Load dataset ===
df = pd.read_csv(file_path)
df['category'] = df['category'].str.lower()
df['motivation'] = df['motivation'].fillna('').astype(str).str.lower()

# === Stopwords personnalisés ===
stopwords = set([
    'for', 'their', 'the', 'and', 'that', 'to', 'of', 'in', 'on', 'by',
    'with', 'as', 'was', 'at', 'an', 'a', 'his', 'her', 'from', 'is'
])

# === Masque (forme) ===
if os.path.exists(mask_path):
    mask_image = np.array(Image.open(mask_path))
else:
    print("⚠️ Aucun masque trouvé. Le wordcloud sera généré en forme classique.")
    mask_image = None

# === Générer un nuage par catégorie ===
categories = df['category'].unique()

for category in categories:
    cat_df = df[df['category'] == category]
    text = ' '.join(cat_df['motivation'])

    # Nettoyage texte
    text = re.sub(r'[^\w\s]', '', text)
    words = [word for word in text.split() if word not in stopwords and len(word) > 3]
    final_text = ' '.join(words)

    # === Générer le wordcloud ===
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        max_words=150,
        colormap='plasma',  # Autres : viridis, inferno, tab10
        contour_color='black',
        contour_width=1,
        mask=mask_image,
        font_path=font_path,
        prefer_horizontal=0.7
    ).generate(final_text)

    # === Dossier de sortie ===
    category_dir = os.path.join(base_output_dir, category)
    if not os.path.exists(category_dir):
        print(f"⚠️ Le dossier {category_dir} n'existe pas. Crée-le manuellement.")
        continue

    output_path = os.path.join(category_dir, f"{category}_motivation_wordcloud.png")

    # === Sauvegarde du nuage ===
    plt.figure(figsize=(14, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f" Motivation — {category.capitalize()}", fontsize=18, weight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"✅ Enregistré : {output_path}")


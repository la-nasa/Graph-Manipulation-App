# Graph Manipulation Pro

**Graph Manipulation Pro** est une application desktop élégante et interactive pour créer, analyser et visualiser des graphes (dirigés ou non), construite en Python avec Tkinter et ttkbootstrap.

---

## Table des matières

1. [Installation](#installation)  
2. [Lancement de l’application](#lancement-de-lapplication)  
3. [Interface générale](#interface-générale)  
4. [Manipulations de base](#manipulations-de-base)  
5. [Algorithmes et animations](#algorithmes-et-animations)  
6. [Fonctions avancées](#fonctions-avancées)  
7. [Import / Export / Reset](#import--export--reset)  
8. [Exemples concrets](#exemples-concrets)

---

## Installation

1. Assurez-vous d’avoir Python >=3.7 d’installé.  
2. (Optionnel) Créez et activez un environnement virtuel :  
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS / Linux
   venv\Scripts\activate       # Windows

3. Installez les dependances:
    pip install networkx matplotlib ttkbootstrap



# Lancement de l’application
Depuis le .py

    python graph_app.py

Depuis l’exécutable Windows
    Double-cliquez sur dist\graph_app.exe.


#   Interface générale
L’interface est divisée en trois zones :

Barre d’onglets (à gauche)

Sépare les fonctionnalités (Nœuds, Arêtes, Algo, Avancé, Divers).

Visualisation du graphe (en haut à droite)

Affiche dynamiquement le graphe.

Panneau de sortie (en bas à droite)

Affiche texte et résultats d’algorithmes.


# Manipulations de base
Ajouter / supprimer des nœuds
Ajouter : saisissez un nom dans “Nom” → Ajouter.

Supprimer : saisissez un nom dans “Supprimer” → Supprimer.

Ajouter / supprimer des arêtes
Ajouter :

Source, Cible (nom de nœuds existants), Poids (optionnel, défaut = 1.0) → Ajouter.

Supprimer :

Saisissez Source et Cible → Supprimer.


#  Algorithmes et animations
Tous les algorithmes s’exécutent dans l’onglet ⚙️ Algo & Anim. Les résultats s’affichent d’abord dans le panneau de sortie, puis l’animation commence.

DFS (Depth-First Search)

Entrez un nœud de départ → DFS Anim.

Résultat : séquence d’arêtes explorées, puis animation sur le graphe.

BFS (Breadth-First Search)

Même usage que la DFS.

Plus court chemin (Dijkstra)

Saisissez “Départ” et “Arrivée” → Dijkstra.

Résultat : chemin et longueur totale.

Composantes connexes

Composantes : affiche les composantes fortement connexes (digraphe) ou simplement connexes.

Détection de cycle

Cycle? : indique “Oui” ou “Non”.

Exemple détaillé (Dijkstra)
Pour un graphe pondéré :
A → B (2), A → C (5), B → C (1), C → D (3)

# Fonctions avancées
Dans l’onglet 🔧 Avancé, vous trouverez :

Centralités

Affiche pour chaque nœud :

Degré, Betweenness centrality, Closeness centrality.

MST (Arbre couvrant minimal)

Pour graphes non orientés (MST (Kruskal)), met en surbrillance les arêtes de l’arbre.

Complément

Affiche le graphe complémentaire (en jaune).

Densité

Indice de densité du graphe (2|E|/(|V|(|V|-1))).
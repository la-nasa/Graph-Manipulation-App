
## **1. Introduction aux graphes**
"""
Un **graphe** est une structure mathématique utilisée pour modéliser des relations entre des objets.

* **Graphe non orienté** : les arêtes n'ont pas de direction.
* **Graphe orienté (digraphe)** : les arêtes ont une direction.
* **Graphe pondéré** : les arêtes ont un poids (coût, distance…).
* **Graphe cyclique** : contient au moins un cycle.
* **Graphe acyclique** : ne contient pas de cycle (ex: arbre).

On utilise souvent la bibliothèque **NetworkX** pour manipuler les graphes en Python.

"""


## **2. Installation**

#pip install networkx matplotlib




## **3. Création d’un graphe**

### **Exemple 1 : Création d’un graphe non orienté simple**


import networkx as nx
import matplotlib.pyplot as plt

# Création d’un graphe non orienté
G = nx.Graph()

# Ajout de sommets (nœuds)
G.add_node("A")
G.add_nodes_from(["B", "C", "D"])

# Ajout d’arêtes
G.add_edge("A", "B")
G.add_edges_from([("B", "C"), ("C", "D"), ("A", "D")])

# Affichage
nx.draw(G, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=15)
plt.title("Graphe simple")
plt.show()




## **4. Graphe orienté et pondéré**

### **Exemple 2 : Création d’un graphe orienté avec poids**


DG = nx.DiGraph()

# Ajout de sommets et d’arêtes avec poids
DG.add_weighted_edges_from([
    ("A", "B", 5),
    ("B", "C", 3),
    ("C", "A", 2),
    ("C", "D", 4)
])

# Affichage avec poids
pos = nx.spring_layout(DG)
nx.draw(DG, pos, with_labels=True, node_color='lightgreen', node_size=2000, arrows=True)
labels = nx.get_edge_attributes(DG, 'weight')
nx.draw_networkx_edge_labels(DG, pos, edge_labels=labels)
plt.title("Graphe orienté pondéré")
plt.show()




## **5. Manipulations des graphes**

### **a) Obtenir les nœuds et arêtes**


print("Nœuds :", DG.nodes())
print("Arêtes :", DG.edges())
print("Arêtes avec poids :", DG.edges(data=True))




### **b) Vérifier l’existence d’un nœud ou d’une arête**


print("A existe ?", 'A' in DG.nodes)
print("Arête A->B existe ?", DG.has_edge("A", "B"))




### **c) Supprimer un nœud ou une arête**


DG.remove_node("D")
DG.remove_edge("C", "A")




### **d) Trouver les voisins (successeurs ou prédécesseurs)**


print("Successeurs de B :", list(DG.successors("B")))
print("Prédécesseurs de C :", list(DG.predecessors("C")))




### **e) Calculer les degrés**


print("Degré entrant de C :", DG.in_degree("C"))
print("Degré sortant de B :", DG.out_degree("B"))




## **6. Algorithmes classiques**

### **a) Parcours en profondeur (DFS)**


dfs_edges = list(nx.dfs_edges(G, source="A"))
print("DFS à partir de A :", dfs_edges)




### **b) Parcours en largeur (BFS)**


bfs_edges = list(nx.bfs_edges(G, source="A"))
print("BFS à partir de A :", bfs_edges)




### **c) Chemin le plus court (Dijkstra)**


# Recréons un graphe pondéré
G_weighted = nx.Graph()
G_weighted.add_weighted_edges_from([
    ("A", "B", 2),
    ("A", "C", 5),
    ("B", "C", 1),
    ("C", "D", 3)
])

path = nx.dijkstra_path(G_weighted, source="A", target="D")
length = nx.dijkstra_path_length(G_weighted, source="A", target="D")

print("Chemin le plus court de A à D :", path)
print("Longueur :", length)




### **d) Détection de cycle**


print("Contient un cycle ? :", nx.is_cycle(G))




### **e) Détection de composantes connexes**

components = list(nx.connected_components(G))
print("Composantes connexes :", components)




### **f) Générer un graphe aléatoire**


RG = nx.gnp_random_graph(5, 0.5)  # 5 nœuds, probabilité 0.5 entre chaque paire
nx.draw(RG, with_labels=True)
plt.title("Graphe aléatoire")
plt.show()




## **7. Exporter et importer un graphe**

### **Exporter vers un fichier GraphML**


nx.write_graphml(G, "graphe.graphml")


### **Lire un fichier GraphML**

G2 = nx.read_graphml("graphe.graphml")
print("Nœuds importés :", G2.nodes())




## **8. Représentation matricielle**

### **Matrice d’adjacence**

A = nx.adjacency_matrix(G).todense()
print("Matrice d’adjacence :\n", A)




### **Matrice d’incidence**


I = nx.incidence_matrix(G, oriented=True).todense()
print("Matrice d’incidence :\n", I)


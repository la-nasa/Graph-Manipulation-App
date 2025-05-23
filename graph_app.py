# graph_app_full.py

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Manipulation By Tatchou Martini and Joh Luna")
        self.root.geometry("1200x700")
        style = tb.Style(theme='superhero')

        # Graphe courant
        self.G = nx.DiGraph()

        # Configuration grille
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)

        # Onglets de commandes
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, rowspan=2, sticky="ns", padx=5, pady=5)

        self._create_node_tab()
        self._create_edge_tab()
        self._create_algo_tab()
        self._create_extra_tab()
        self._create_misc_tab()

        # Canvas Matplotlib pour graphe
        self.fig, self.ax = plt.subplots(figsize=(6,6), facecolor=style.colors.bg)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Panneau de sortie (résultats)
        self.output = scrolledtext.ScrolledText(self.root, wrap='word', height=10, state='disabled', font=("Consolas", 10))
        self.output.grid(row=1, column=1, sticky="nsew", padx=5, pady=(0,5))

        # Affichage initial
        self._draw_graph()

    # onglet Nœuds
    def _create_node_tab(self):
        f = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(f, text="🔘 Nœuds")
        ttk.Label(f, text="Nom :").grid(row=0, column=0, sticky="w", pady=3)
        self.node_name = ttk.Entry(f); self.node_name.grid(row=0, column=1, sticky="ew", pady=3)
        tb.Button(f, text="Ajouter", bootstyle="success-outline", command=self.add_node).grid(row=0, column=2, padx=5)
        ttk.Label(f, text="Supprimer :").grid(row=1, column=0, sticky="w", pady=3)
        self.node_remove = ttk.Entry(f); self.node_remove.grid(row=1, column=1, sticky="ew", pady=3)
        tb.Button(f, text="Supprimer", bootstyle="danger-outline", command=self.remove_node).grid(row=1, column=2, padx=5)
        f.columnconfigure(1, weight=1)

    def add_node(self):
        name = self.node_name.get().strip()
        if name:
            self.G.add_node(name)
            self.node_name.delete(0, tk.END)
            self._draw_graph()
        else:
            self._log("⚠️ Nom de nœud vide !")

    def remove_node(self):
        name = self.node_remove.get().strip()
        if name in self.G:
            self.G.remove_node(name)
            self.node_remove.delete(0, tk.END)
            self._draw_graph()
        else:
            self._log(f"⚠️ Nœud '{name}' introuvable.")

    # onglet Arêtes 
    def _create_edge_tab(self):
        f = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(f, text="➡️ Arêtes")
        for i, lbl in enumerate(["Source","Cible","Poids"]):
            ttk.Label(f, text=lbl+":").grid(row=0, column=2*i, sticky="w", pady=3)
        self.edge_src = ttk.Entry(f); self.edge_src.grid(row=0, column=1, sticky="ew", pady=3)
        self.edge_dst = ttk.Entry(f); self.edge_dst.grid(row=0, column=3, sticky="ew", pady=3)
        self.edge_w   = ttk.Entry(f); self.edge_w.grid(row=0, column=5, sticky="ew", pady=3)
        tb.Button(f, text="Ajouter", bootstyle="primary-outline", command=self.add_edge).grid(row=1, column=1, pady=5)
        ttk.Label(f, text="Suppr src→dst :").grid(row=2, column=0, sticky="w", pady=3)
        self.edge_rm_src = ttk.Entry(f); self.edge_rm_src.grid(row=2, column=1, sticky="ew", pady=3)
        self.edge_rm_dst = ttk.Entry(f); self.edge_rm_dst.grid(row=2, column=3, sticky="ew", pady=3)
        tb.Button(f, text="Supprimer", bootstyle="danger-outline", command=self.remove_edge).grid(row=2, column=5, padx=5)
        f.columnconfigure(1, weight=1); f.columnconfigure(3, weight=1); f.columnconfigure(5, weight=1)

    def add_edge(self):
        u,v,w = self.edge_src.get().strip(), self.edge_dst.get().strip(), self.edge_w.get().strip()
        if u and v:
            try:
                wt = float(w) if w else 1.0
                self.G.add_edge(u, v, weight=wt)
                self.edge_src.delete(0,tk.END); self.edge_dst.delete(0,tk.END); self.edge_w.delete(0,tk.END)
                self._draw_graph()
            except ValueError:
                self._log("⚠️ Poids invalide.")
        else:
            self._log("⚠️ Source ou cible vide.")

    def remove_edge(self):
        u,v = self.edge_rm_src.get().strip(), self.edge_rm_dst.get().strip()
        if self.G.has_edge(u, v):
            self.G.remove_edge(u, v)
            self.edge_rm_src.delete(0,tk.END); self.edge_rm_dst.delete(0,tk.END)
            self._draw_graph()
        else:
            self._log(f"⚠️ Arête {u}→{v} introuvable.")

    #  onglet Algorithmes & Anim 
    def _create_algo_tab(self):
        f = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(f, text="⚙️ Algo & Anim")
        ttk.Label(f, text="Source :").grid(row=0, column=0, sticky="w", pady=3)
        self.algo_src = ttk.Entry(f); self.algo_src.grid(row=0, column=1, sticky="ew", pady=3)
        tb.Button(f, text="DFS Anim",  bootstyle="info-outline", command=lambda:self.prepare_and_animate('dfs')).grid(row=0, column=2, padx=5)
        tb.Button(f, text="BFS Anim",  bootstyle="info-outline", command=lambda:self.prepare_and_animate('bfs')).grid(row=0, column=3, padx=5)
        ttk.Label(f, text="Départ :").grid(row=1, column=0, sticky="w", pady=3)
        self.dp_src = ttk.Entry(f); self.dp_src.grid(row=1, column=1, sticky="ew", pady=3)
        ttk.Label(f, text="Arrivée :").grid(row=1, column=2, sticky="w", pady=3)
        self.dp_dst = ttk.Entry(f); self.dp_dst.grid(row=1, column=3, sticky="ew", pady=3)
        tb.Button(f, text="Dijkstra", bootstyle="warning-outline", command=self.run_dijkstra).grid(row=1, column=4, padx=5)
        tb.Button(f, text="Composantes", bootstyle="secondary-outline", command=self.show_components).grid(row=2, column=0, pady=5)
        tb.Button(f, text="Cycle?",       bootstyle="secondary-outline", command=self.check_cycle).grid(row=2, column=1, pady=5)
        f.columnconfigure(1, weight=1); f.columnconfigure(3, weight=1)

    def prepare_and_animate(self, mode):
        src = self.algo_src.get().strip()
        if src not in self.G:
            return self._log(f"⚠️ Nœud {src} introuvable.")
        # Calcul et affichage avant animation
        seq = list(nx.dfs_edges(self.G, source=src)) if mode=='dfs' else list(nx.bfs_edges(self.G, source=src))
        self._log(f"{mode.upper()} sequence: {seq}")
        # Lancement animation
        threading.Thread(target=self._run_animation, args=(seq,), daemon=True).start()

    def _run_animation(self, seq):
        for u,v in seq:
            self.ax.clear()
            pos = nx.spring_layout(self.G, seed=42)
            nx.draw(self.G, pos, ax=self.ax, node_color='lightgray', with_labels=True)
            nx.draw_networkx_edges(self.G, pos, edgelist=[(u,v)], edge_color='cyan', width=3, ax=self.ax, arrowstyle='->')
            self.canvas.draw()
            time.sleep(0.6)
        self._draw_graph()

    def run_dijkstra(self):
        u,v = self.dp_src.get().strip(), self.dp_dst.get().strip()
        if u in self.G and v in self.G:
            try:
                path = nx.dijkstra_path(self.G, u, v)
                L    = nx.dijkstra_path_length(self.G, u, v)
                self._log(f"Dijkstra {u}->{v}: chemin={path}, longueur={L}")
            except nx.NetworkXNoPath:
                self._log("⚠️ Pas de chemin.")
        else:
            self._log("⚠️ Nœuds invalides.")

    def show_components(self):
        comps = (list(nx.strongly_connected_components(self.G)) 
                 if self.G.is_directed() else list(nx.connected_components(self.G)))
        self._log(f"Composantes: {comps}")

    def check_cycle(self):
        cyc = (list(nx.simple_cycles(self.G)) 
               if self.G.is_directed() else nx.cycle_basis(self.G))
        self._log(f"Présence de cycle: {'Oui' if cyc else 'Non'}")

    #  onglet Avancé 
    def _create_extra_tab(self):
        f = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(f, text="🔧 Avancé")
        tb.Button(f, text="Centralités",      bootstyle="info-outline",    command=self.show_centralities).grid(row=0, column=0, pady=5, padx=5)
        tb.Button(f, text="MST (Kruskal)",    bootstyle="success-outline", command=self.show_mst).grid(row=0, column=1, pady=5, padx=5)
        tb.Button(f, text="Complément",       bootstyle="secondary-outline",command=self.show_complement).grid(row=1, column=0, pady=5, padx=5)
        tb.Button(f, text="Densité",          bootstyle="secondary-outline",command=self.show_density).grid(row=1, column=1, pady=5, padx=5)
        f.columnconfigure(0, weight=1); f.columnconfigure(1, weight=1)

    def show_centralities(self):
        deg = dict(self.G.degree())
        btw = nx.betweenness_centrality(self.G)
        clo = nx.closeness_centrality(self.G)
        lines = [f"{n}: deg={deg[n]:.2f}, btw={btw[n]:.2f}, clo={clo[n]:.2f}" for n in self.G.nodes()]
        self._log("Centralités:\n" + "\n".join(lines) if lines else "Graphe vide.")

    def show_mst(self):
        if not self.G.is_directed():
            T = nx.minimum_spanning_tree(self.G)
            self._highlight_subgraph(T, "MST")
            self._log("MST mis en évidence.")
        else:
            self._log("⚠️ MST disponible que sur graphes non orientés.")

    def show_complement(self):
        C = nx.complement(self.G.to_undirected())
        self._highlight_subgraph(C, "Complément")
        self._log("Complément mis en évidence.")

    def show_density(self):
        d = nx.density(self.G)
        self._log(f"Densité: {d:.4f}")

    def _highlight_subgraph(self, H, title):
        self.ax.clear()
        pos = nx.spring_layout(self.G, seed=42)
        nx.draw(self.G, pos, ax=self.ax, node_color='lightgray', with_labels=True)
        nx.draw_networkx_edges(H, pos, ax=self.ax, edge_color='yellow', width=3)
        self.canvas.draw()

    #  onglet Divers & Réinitialiser 
    def _create_misc_tab(self):
        f = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(f, text="📁 Divers")
        ttk.Label(f, text="nœuds :").grid(row=0, column=0, sticky="w", pady=3)
        self.rand_n = ttk.Entry(f); self.rand_n.grid(row=0, column=1, sticky="ew", pady=3)
        ttk.Label(f, text="p :").grid(row=0, column=2, sticky="w", pady=3)
        self.rand_p = ttk.Entry(f); self.rand_p.grid(row=0, column=3, sticky="ew", pady=3)
        tb.Button(f, text="Générer", bootstyle="warning-outline", command=self.random_graph).grid(row=0, column=4, padx=5)
        tb.Button(f, text="Importer .graphml", bootstyle="primary-outline", command=self.import_graphml).grid(row=1, column=0, columnspan=2, pady=5)
        tb.Button(f, text="Exporter .graphml", bootstyle="success-outline", command=self.export_graphml).grid(row=1, column=2, columnspan=2, pady=5)
        tb.Button(f, text="Réinitialiser", bootstyle="danger-outline", command=self.reset_graph).grid(row=2, column=0, columnspan=5, pady=10)
        f.columnconfigure(1, weight=1); f.columnconfigure(3, weight=1)

    def random_graph(self):
        try:
            n, p = int(self.rand_n.get()), float(self.rand_p.get())
            self.G = nx.gnp_random_graph(n, p, directed=True)
            self._draw_graph()
            self._log(f"Graphe aléatoire généré: n={n}, p={p}")
        except Exception:
            self._log("⚠️ Paramètres invalides.")

    def import_graphml(self):
        path = filedialog.askopenfilename(filetypes=[("GraphML","*.graphml")])
        if path:
            self.G = nx.read_graphml(path)
            self._draw_graph()
            self._log(f"Importé: {path}")

    def export_graphml(self):
        path = filedialog.asksaveasfilename(defaultextension=".graphml", filetypes=[("GraphML","*.graphml")])
        if path:
            nx.write_graphml(self.G, path)
            self._log(f"Exporté: {path}")

    def reset_graph(self):
        self.G.clear()
        self._draw_graph()
        self._log("🔄 Graphe réinitialisé.")

    # dessin & utils 
    def _draw_graph(self):
        self.ax.clear()
        if not self.G.nodes:
            self.ax.text(0.5,0.5,"Graph vide",ha="center",va="center",fontsize=18,color='gray')
        else:
            pos = nx.spring_layout(self.G, seed=42)
            weights = nx.get_edge_attributes(self.G,'weight')
            nx.draw_networkx_nodes(self.G, pos, ax=self.ax, node_size=400, node_color='skyblue')
            nx.draw_networkx_edges(self.G, pos, ax=self.ax, arrowstyle='->', arrowsize=12)
            nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=10)
            if weights:
                nx.draw_networkx_edge_labels(self.G, pos, edge_labels=weights, ax=self.ax)
        self.ax.set_axis_off()
        self.canvas.draw()

    def _log(self, text: str):
        """Insère une ligne dans le panneau de sortie."""
        self.output.configure(state='normal')
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state='disabled')


if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = GraphApp(root)
    root.mainloop()


from graphviz import Digraph


class HuffmanTreeViewer:
    def __init__(self, root, output_filename="huffman_tree.png"):
        self.root = root
        self.output_filename = output_filename
        self.graph = Digraph(format="png")
        self.graph.attr(size="15,15")

    def _add_nodes_edges(self, node, parent_name=None, edge_label=""):
        if node is None:
            return

        node_name = str(id(node))
        if node.is_leaf():
            self.graph.node(node_name, label=f"{node.char} ({node.freq})")
        else:
            self.graph.node(node_name, label=f"{node.freq}")

        if parent_name:
            self.graph.edge(parent_name, node_name, label=edge_label)

        self._add_nodes_edges(node.left, node_name, "0")
        self._add_nodes_edges(node.right, node_name, "1")

    def generate_tree_visualization(self):
        self._add_nodes_edges(self.root)
        print(f"Árvore de Huffman gerada e salva em '{self.output_filename}'")
        return self.graph.render(cleanup=True)

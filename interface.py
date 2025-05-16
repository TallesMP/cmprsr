
import easygui
import os
from huffman import HuffmanCompressor
from HuffmanTreeViewer import HuffmanTreeViewer


def mostrar_resultado(orig, comprimido):
    msg = f"Tamanho original: {
        orig} bytes\nTamanho comprimido: {comprimido} bytes\n"
    easygui.msgbox(msg, title="Resultado")


def visualizar_arvore(root):
    visualizer = HuffmanTreeViewer(root)
    arvore_path = visualizer.generate_tree_visualization()
    easygui.msgbox("Árvore de Huffman gerada!",
                   title="Visualização da Árvore", image=arvore_path)


def mostrar_texto(original_text):
    easygui.textbox("Texto original descomprimido:",
                    "Mensagem Original", original_text)


def main():
    while True:
        escolha = easygui.buttonbox(
            "O que gostaria de fazer?", "Bem-vindo!", [
                "Comprimir", "Descomprimir", "Ver árvore", "Sair"]
        )

        if escolha is None or escolha == "Sair":
            break

        if escolha == "Comprimir":
            arquivo = easygui.fileopenbox(
                "Selecione o arquivo para compactar:")
            if not arquivo:
                continue

            compressor = HuffmanCompressor(arquivo)
            compressor.compress()

            tamanho_original = os.path.getsize(arquivo)
            tamanho_comprimido = os.path.getsize(
                compressor.compressed_filename)

            mostrar_resultado(tamanho_original, tamanho_comprimido)

        elif escolha == "Descomprimir":
            arquivo_comprimido = easygui.fileopenbox(
                "Selecione o arquivo comprimido:")
            if not arquivo_comprimido:
                continue

            compressor = HuffmanCompressor(
                compressed_filename=arquivo_comprimido)
            compressor.decompress()

            original_text = compressor.decode_text()
            mostrar_texto(original_text)

        elif escolha == "Ver árvore":
            arquivo = easygui.fileopenbox(
                "Selecione o arquivo original para visualizar a árvore:")
            if not arquivo:
                continue

            compressor = HuffmanCompressor(arquivo)
            compressor.build_huffman_tree()
            visualizar_arvore(compressor.root)

    print("Programa encerrado.")


if __name__ == "__main__":
    main()

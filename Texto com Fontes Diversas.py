import tkinter as tk
from tkinter import font, colorchooser

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto Personalizado")
        self.root.geometry("600x400")
        
        self.text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH)

        self.create_buttons()

        # Definindo as tags para o estilo
        self.text_area.tag_configure("bold", font=("Arial", 12, "bold"))
        self.text_area.tag_configure("italic", font=("Arial", 12, "italic"))
        self.text_area.tag_configure("underline", font=("Arial", 12, "underline"))
        self.text_area.tag_configure("size", font=("Arial", 12))  # Tamanho da fonte
        self.text_area.tag_configure("color", foreground="black")  # Cor do texto

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X)

        # Botão para escolher a cor do texto
        color_button = tk.Button(button_frame, text="Cor do Texto", command=self.change_color)
        color_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Botão para aumentar o tamanho da fonte
        increase_button = tk.Button(button_frame, text="Aumentar Fonte", command=self.increase_font_size)
        increase_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Botão para diminuir o tamanho da fonte
        decrease_button = tk.Button(button_frame, text="Diminuir Fonte", command=self.decrease_font_size)
        decrease_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Botão para negrito
        bold_button = tk.Button(button_frame, text="Negrito", command=self.toggle_bold)
        bold_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Botão para itálico
        italic_button = tk.Button(button_frame, text="Itálico", command=self.toggle_italic)
        italic_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Botão para sublinhado
        underline_button = tk.Button(button_frame, text="Sublinhado", command=self.toggle_underline)
        underline_button.pack(side=tk.LEFT, padx=5, pady=5)

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self._apply_tag_with_color("color", color)

    def increase_font_size(self):
        self._change_font_size(2)

    def decrease_font_size(self):
        self._change_font_size(-2)

    def _change_font_size(self, delta):
        try:
            start, end = self.text_area.index("sel.first"), self.text_area.index("sel.last")
            current_font = font.Font(font=self.text_area.tag_cget("size", "font"))
            new_size = max(current_font.actual("size") + delta, 1)  # Evitar tamanho 0
            new_font = (current_font.actual("family"), new_size)

            # Aplicar a mudança de tamanho mantendo as tags de estilo
            self.text_area.tag_configure("size", font=new_font)
            self.text_area.tag_add("size", start, end)
        except tk.TclError:
            pass  # Ignorar se nada estiver selecionado

    def toggle_bold(self):
        self._toggle_tag("bold")

    def toggle_italic(self):
        self._toggle_tag("italic")

    def toggle_underline(self):
        self._toggle_tag("underline")

    def _toggle_tag(self, tag):
        """Ativa ou desativa uma tag na seleção atual."""
        try:
            start, end = self.text_area.index("sel.first"), self.text_area.index("sel.last")
            if tag in self.text_area.tag_names("sel.first"):
                self.text_area.tag_remove(tag, start, end)
            else:
                self.text_area.tag_add(tag, start, end)
        except tk.TclError:
            pass  # Ignorar se nada estiver selecionado

    def _apply_tag_with_color(self, tag, color):
        """Aplica a cor apenas no texto selecionado e não no restante do conteúdo."""
        try:
            start, end = self.text_area.index("sel.first"), self.text_area.index("sel.last")
            # Manter as tags existentes (negrito, itálico, sublinhado) ao aplicar a cor
            existing_tags = self.text_area.tag_names(start)
            self.text_area.tag_add(tag, start, end)
            self.text_area.tag_configure(tag, foreground=color)  # Configura a cor somente para a seleção

            # Reaplicar todas as outras tags ao texto selecionado
            for existing_tag in existing_tags:
                if existing_tag != tag:  # Evitar aplicar a tag de cor novamente
                    self.text_area.tag_add(existing_tag, start, end)
        except tk.TclError:
            pass  # Ignorar se nada estiver selecionado

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()

import wx
import wx.richtext as rt

class TextEditorApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))

        self.panel = wx.Panel(self)

        # Cria o campo de texto rico
        self.text_ctrl = rt.RichTextCtrl(self.panel, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER, size=(780, 500))
        self.text_ctrl.SetBackgroundColour("white")

        # Botões de formatação
        self.create_buttons()

        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 10)
        vbox.Add(self.button_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def create_buttons(self):
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Botões de ação
        buttons = [
            ("Cor", self.change_color),
            ("Aumentar Fonte", self.increase_font),
            ("Diminuir Fonte", self.decrease_font),
            ("Negrito", self.toggle_bold),
            ("Itálico", self.toggle_italic),
            ("Sublinhado", self.toggle_underline),
        ]

        for label, handler in buttons:
            button = wx.Button(self.panel, label=label)
            button.Bind(wx.EVT_BUTTON, handler)
            self.button_sizer.Add(button, 0, wx.ALL, 5)

    def get_selection(self):
        """Obtém a seleção atual no controle de texto."""
        selection = self.text_ctrl.GetSelectionRange()
        return selection.GetStart(), selection.GetEnd()

    def apply_style(self, attr):
        """Aplica um estilo ao texto selecionado."""
        start, end = self.get_selection()
        if start != end:  # Apenas aplica estilo se houver texto selecionado
            self.text_ctrl.SetStyle(start, end, attr)

    def change_color(self, event):
        """Muda a cor do texto selecionado."""
        color_dialog = wx.ColourDialog(self)
        if color_dialog.ShowModal() == wx.ID_OK:
            color = color_dialog.GetColourData().GetColour()
            attr = wx.TextAttr()
            attr.SetTextColour(color)
            self.apply_style(attr)

    def increase_font(self, event):
        """Aumenta o tamanho da fonte do texto selecionado."""
        start, end = self.get_selection()
        if start != end:
            for pos in range(start, end):
                attr = wx.TextAttr()
                if self.text_ctrl.GetStyle(pos, attr):
                    font = attr.GetFont()
                    font.SetPointSize(font.GetPointSize() + 1)
                    attr.SetFont(font)
                    self.text_ctrl.SetStyle(pos, pos + 1, attr)

    def decrease_font(self, event):
        """Diminui o tamanho da fonte do texto selecionado."""
        start, end = self.get_selection()
        if start != end:
            for pos in range(start, end):
                attr = wx.TextAttr()
                if self.text_ctrl.GetStyle(pos, attr):
                    font = attr.GetFont()
                    font.SetPointSize(max(1, font.GetPointSize() - 1))
                    attr.SetFont(font)
                    self.text_ctrl.SetStyle(pos, pos + 1, attr)

    def toggle_bold(self, event):
        """Alterna o estilo negrito no texto selecionado."""
        start, end = self.get_selection()
        if start != end:
            for pos in range(start, end):
                attr = wx.TextAttr()
                if self.text_ctrl.GetStyle(pos, attr):
                    font = attr.GetFont()
                    font.SetWeight(wx.FONTWEIGHT_NORMAL if font.GetWeight() == wx.FONTWEIGHT_BOLD else wx.FONTWEIGHT_BOLD)
                    attr.SetFont(font)
                    self.text_ctrl.SetStyle(pos, pos + 1, attr)

    def toggle_italic(self, event):
        """Alterna o estilo itálico no texto selecionado."""
        start, end = self.get_selection()
        if start != end:
            for pos in range(start, end):
                attr = wx.TextAttr()
                if self.text_ctrl.GetStyle(pos, attr):
                    font = attr.GetFont()
                    font.SetStyle(wx.FONTSTYLE_NORMAL if font.GetStyle() == wx.FONTSTYLE_ITALIC else wx.FONTSTYLE_ITALIC)
                    attr.SetFont(font)
                    self.text_ctrl.SetStyle(pos, pos + 1, attr)

    def toggle_underline(self, event):
        """Alterna o estilo sublinhado no texto selecionado."""
        start, end = self.get_selection()
        if start != end:
            for pos in range(start, end):
                attr = wx.TextAttr()
                if self.text_ctrl.GetStyle(pos, attr):
                    font = attr.GetFont()
                    font.SetUnderlined(not font.GetUnderlined())
                    attr.SetFont(font)
                    self.text_ctrl.SetStyle(pos, pos + 1, attr)

if __name__ == "__main__":
    app = wx.App(False)
    frame = TextEditorApp(None, title="Editor de Texto Personalizado")
    app.MainLoop()

Label:
        text: "Submit your picture!"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top":1}

    Button:
        text: "Submit your picture!"
        size_hint: 0.8, 0.2
        pos_hint: {"x":0.2, "y":0.1}


id: my_widget
    FileChooserListView:
        id: filechooser
        on_selection: my_widget.selected(filechooser.selection)
    Image:
        id: image
        source: ""
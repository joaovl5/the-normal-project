import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x50")
        self.resizable(False, False)
        self.title("Instalador do launcher bem normal!")

        self.progressbar = customtkinter.CTkProgressBar(
            self, orientation="horizontal", width=380
        )
        self.progressbar.set(0)
        self.progressbar.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

        self.label = customtkinter.CTkLabel(self, text="0%", fg_color="transparent")
        self.label.place(relx=0.5, rely=0.625, anchor=customtkinter.CENTER)

    def update_progress(self, value: float):
        self.label.configure(text=f"{round(value*100)}%")
        self.progressbar.set(value)

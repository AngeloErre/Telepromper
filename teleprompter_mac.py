#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
from pathlib import Path
import time


class TeleprompterApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Teleprompter")
        self.root.geometry("1200x780")
        self.root.minsize(800, 500)
        self.root.configure(bg="#111111")

        # Stato del programma
        self.running = False
        self.fullscreen = False

        # Cronometro
        self.elapsed = 0.0
        self.last_tick = None

        # Scorrimento
        self.scroll_accumulator = 0.0
        self.last_scroll_time = time.monotonic()

        self.current_file = None

        # Variabili interfaccia
        self.font_family = tk.StringVar(value="Helvetica")
        self.font_size = tk.IntVar(value=42)
        self.speed = tk.DoubleVar(value=30.0)

        self.status_text = tk.StringVar(value="PRONTO")
        self.timer_text = tk.StringVar(value="00:00")

        self.build_ui()
        self.populate_fonts()
        self.bind_keys()
        self.update_text_font()

        self.animation_loop()

    # --------------------------------------------------
    # INTERFACCIA
    # --------------------------------------------------

    def build_ui(self):

        self.toolbar = tk.Frame(
            self.root,
            bg="#222222",
            padx=10,
            pady=8
        )

        self.toolbar.pack(
            side="top",
            fill="x"
        )

        # Apertura TXT
        tk.Button(
            self.toolbar,
            text="Apri TXT",
            command=self.load_txt,
            bg="#333333",
            fg="white",
            relief="flat",
            padx=12,
            pady=6
        ).pack(side="left", padx=(0, 10))

        # Font
        tk.Label(
            self.toolbar,
            text="Font:",
            bg="#222222",
            fg="white"
        ).pack(side="left")

        self.font_menu = tk.OptionMenu(
            self.toolbar,
            self.font_family,
            "Helvetica"
        )

        self.font_menu.config(
            bg="#333333",
            fg="white",
            highlightthickness=0,
            width=18
        )

        self.font_menu.pack(
            side="left",
            padx=(4, 10)
        )

        # Dimensione
        tk.Label(
            self.toolbar,
            text="Dimensione:",
            bg="#222222",
            fg="white"
        ).pack(side="left")

        self.size_spin = tk.Spinbox(
            self.toolbar,
            from_=16,
            to=120,
            textvariable=self.font_size,
            width=4,
            command=self.update_text_font,
            bg="#333333",
            fg="white"
        )

        self.size_spin.pack(
            side="left",
            padx=(4, 12)
        )

        self.size_spin.bind(
            "<KeyRelease>",
            lambda event: self.update_text_font()
        )

        # Velocità
        tk.Label(
            self.toolbar,
            text="Velocità:",
            bg="#222222",
            fg="white"
        ).pack(side="left")

        self.speed_scale = tk.Scale(
            self.toolbar,
            from_=5,
            to=150,
            orient="horizontal",
            variable=self.speed,
            length=170,
            bg="#222222",
            fg="white",
            troughcolor="#444444",
            highlightthickness=0
        )

        self.speed_scale.pack(
            side="left",
            padx=(4, 12)
        )

        # Schermo intero
        tk.Button(
            self.toolbar,
            text="Schermo intero (F)",
            command=self.toggle_fullscreen,
            bg="#333333",
            fg="white",
            relief="flat",
            padx=10,
            pady=6
        ).pack(side="left", padx=5)

        # Barra informazioni
        self.info_frame = tk.Frame(
            self.root,
            bg="#111111",
            padx=16,
            pady=8
        )

        self.info_frame.pack(
            side="top",
            fill="x"
        )

        tk.Label(
            self.info_frame,
            textvariable=self.status_text,
            font=("Helvetica", 13, "bold"),
            bg="#111111",
            fg="#bbbbbb"
        ).pack(side="left")

        tk.Label(
            self.info_frame,
            textvariable=self.timer_text,
            font=("Menlo", 22, "bold"),
            bg="#111111",
            fg="white"
        ).pack(side="right")

        # Area testo
        text_frame = tk.Frame(
            self.root,
            bg="#111111"
        )

        text_frame.pack(
            fill="both",
            expand=True
        )

        self.text = tk.Text(
            text_frame,
            wrap="word",
            bg="#111111",
            fg="#f4f4f4",
            insertbackground="white",
            selectbackground="#444444",
            relief="flat",
            borderwidth=0,
            padx=80,
            pady=70,
            spacing1=8,
            spacing2=4,
            spacing3=20,
            cursor="arrow"
        )

        self.text.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar = tk.Scrollbar(
            text_frame,
            command=self.text.yview
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.text.configure(
            yscrollcommand=self.scrollbar.set
        )

        # Testo iniziale
        self.text.insert(
            "1.0",
            "TELEPROMPTER\n\n"
            "Carica un file .txt con il pulsante Apri TXT.\n\n"
            "SPAZIO — Avvia / Pausa\n"
            "X — Torna all'inizio\n"
            "F — Schermo intero\n"
            "ESC — Esci dallo schermo intero\n\n"
            "La velocità può essere modificata durante la lettura."
        )

        self.text.configure(state="disabled")

        # Footer
        self.footer = tk.Label(
            self.root,
            text=(
                "SPAZIO  Avvia/Pausa     •     "
                "X  Riparti dall'inizio     •     "
                "F  Schermo intero     •     "
                "ESC  Esci"
            ),
            bg="#222222",
            fg="#aaaaaa",
            font=("Helvetica", 11),
            pady=7
        )

        self.footer.pack(
            side="bottom",
            fill="x"
        )

        self.font_family.trace_add(
            "write",
            lambda *_: self.update_text_font()
        )

        self.font_size.trace_add(
            "write",
            lambda *_: self.update_text_font()
        )

    # --------------------------------------------------
    # FONT
    # --------------------------------------------------

    def populate_fonts(self):

        families = sorted(
            set(tkfont.families())
        )

        preferred = [
            "Helvetica",
            "Arial",
            "Avenir",
            "Menlo",
            "Georgia",
            "Times New Roman"
        ]

        default = next(
            (f for f in preferred if f in families),
            families[0] if families else "Helvetica"
        )

        self.font_family.set(default)

        menu = self.font_menu["menu"]
        menu.delete(0, "end")

        for family in families:

            menu.add_command(
                label=family,
                command=lambda f=family: self.font_family.set(f)
            )

    def update_text_font(self):

        try:
            size = int(self.font_size.get())

        except (ValueError, tk.TclError):
            return

        family = self.font_family.get() or "Helvetica"

        self.text.configure(
            font=(family, size)
        )

    # --------------------------------------------------
    # CARICAMENTO FILE TXT
    # --------------------------------------------------

    def load_txt(self):

        path = filedialog.askopenfilename(
            title="Seleziona il testo del teleprompter",
            filetypes=[
                ("File di testo", "*.txt"),
                ("Tutti i file", "*.*")
            ]
        )

        if not path:
            return

        try:

            # Lettura UTF-8
            try:
                content = Path(path).read_text(
                    encoding="utf-8-sig"
                )

            except UnicodeDecodeError:

                # Compatibilità con altri file di testo
                content = Path(path).read_text(
                    encoding="cp1252"
                )

            self.text.configure(state="normal")

            self.text.delete(
                "1.0",
                "end"
            )

            self.text.insert(
                "1.0",
                content
            )

            self.text.configure(state="disabled")

            self.current_file = path

            self.root.title(
                f"Teleprompter — {Path(path).name}"
            )

            self.reset()

        except Exception as exc:

            messagebox.showerror(
                "Errore",
                f"Impossibile aprire il file:\n{exc}"
            )

    # --------------------------------------------------
    # TASTIERA
    # --------------------------------------------------

    def bind_keys(self):

        self.root.bind_all(
            "<space>",
            self.toggle_play
        )

        self.root.bind_all(
            "<KeyPress-x>",
            self.reset
        )

        self.root.bind_all(
            "<KeyPress-X>",
            self.reset
        )

        self.root.bind_all(
            "<KeyPress-f>",
            self.toggle_fullscreen
        )

        self.root.bind_all(
            "<KeyPress-F>",
            self.toggle_fullscreen
        )

        self.root.bind_all(
            "<Escape>",
            self.exit_fullscreen
        )

    # --------------------------------------------------
    # AVVIO / PAUSA
    # --------------------------------------------------

    def toggle_play(self, event=None):

        self.running = not self.running

        now = time.monotonic()

        self.last_scroll_time = now

        if self.running:

            self.last_tick = now
            self.status_text.set("IN LETTURA")

        else:

            if self.last_tick is not None:
                self.elapsed += now - self.last_tick

            self.last_tick = None

            self.status_text.set("PAUSA")

        self.update_timer_display()

        return "break"

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self, event=None):

        self.running = False

        self.elapsed = 0.0

        self.last_tick = None

        self.scroll_accumulator = 0.0

        self.last_scroll_time = time.monotonic()

        self.text.yview_moveto(0.0)

        self.status_text.set("PRONTO")

        self.update_timer_display()

        return "break"

    # --------------------------------------------------
    # SCHERMO INTERO
    # --------------------------------------------------

    def toggle_fullscreen(self, event=None):

        self.fullscreen = not self.fullscreen

        self.root.attributes(
            "-fullscreen",
            self.fullscreen
        )

        if self.fullscreen:

            self.toolbar.pack_forget()
            self.footer.pack_forget()

        else:

            self.toolbar.pack(
                side="top",
                fill="x",
                before=self.info_frame
            )

            self.footer.pack(
                side="bottom",
                fill="x"
            )

        return "break"

    def exit_fullscreen(self, event=None):

        if self.fullscreen:

            self.fullscreen = False

            self.root.attributes(
                "-fullscreen",
                False
            )

            self.toolbar.pack(
                side="top",
                fill="x",
                before=self.info_frame
            )

            self.footer.pack(
                side="bottom",
                fill="x"
            )

        return "break"

    # --------------------------------------------------
    # TIMER
    # --------------------------------------------------

    def update_timer_display(self):

        total = self.elapsed

        if self.running and self.last_tick is not None:

            total += time.monotonic() - self.last_tick

        seconds = max(
            0,
            int(total)
        )

        hours, rem = divmod(
            seconds,
            3600
        )

        minutes, secs = divmod(
            rem,
            60
        )

        if hours:

            self.timer_text.set(
                f"{hours:02d}:{minutes:02d}:{secs:02d}"
            )

        else:

            self.timer_text.set(
                f"{minutes:02d}:{secs:02d}"
            )

    # --------------------------------------------------
    # SCORRIMENTO AUTOMATICO
    # --------------------------------------------------

    def animation_loop(self):

        now = time.monotonic()

        if self.running:

            dt = min(
                now - self.last_scroll_time,
                0.1
            )

            self.scroll_accumulator += (
                float(self.speed.get()) * dt
            )

            pixels = int(
                self.scroll_accumulator
            )

            if pixels > 0:

                before = self.text.yview()

                self.text.yview_scroll(
                    pixels,
                    "pixels"
                )

                after = self.text.yview()

                self.scroll_accumulator -= pixels

                # Pausa automatica alla fine
                if (
                    after[1] >= 0.999999
                    and before == after
                ):

                    self.toggle_play()

        self.last_scroll_time = now

        self.update_timer_display()

        self.root.after(
            16,
            self.animation_loop
        )


# --------------------------------------------------
# AVVIO APPLICAZIONE
# --------------------------------------------------

def main():

    root = tk.Tk()

    app = TeleprompterApp(root)

    root.mainloop()


if __name__ == "__main__":

    main()
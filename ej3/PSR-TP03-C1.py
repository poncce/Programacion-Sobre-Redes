import tkinter as tk
import threading
import random
import time

N = 1000
COLORS = [
    "#E24B4A", "#E8733A", "#EF9F27", "#97C459", "#1D9E75",
    "#378ADD", "#7F77DD", "#D4537E", "#888780", "#5DCAA5",
]
ALG_COLORS = ["#E24B4A", "#378ADD", "#1D9E75", "#7F77DD"]
ALG_NAMES  = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Quick Sort"]

CANVAS_W = 500
CANVAS_H = 180
DELAY    = 0.0   


def bubble_sort(arr, draw_cb, stats):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            stats["comps"] += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                stats["swaps"] += 1
                swapped = True
            if stats["comps"] % 80 == 0:
                draw_cb(arr, [j, j + 1], stats)
                if DELAY: time.sleep(DELAY)
        if not swapped:
            break
    draw_cb(arr, [], stats)


def selection_sort(arr, draw_cb, stats):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            stats["comps"] += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
            if stats["comps"] % 100 == 0:
                draw_cb(arr, [i, j], stats)
                if DELAY: time.sleep(DELAY)
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            stats["swaps"] += 1
        draw_cb(arr, [i, min_idx], stats)
    draw_cb(arr, [], stats)


def insertion_sort(arr, draw_cb, stats):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            stats["comps"] += 1
            arr[j + 1] = arr[j]
            stats["swaps"] += 1
            j -= 1
            if stats["swaps"] % 60 == 0:
                draw_cb(arr, [j + 1, i], stats)
                if DELAY: time.sleep(DELAY)
        arr[j + 1] = key
        if i % 20 == 0:
            draw_cb(arr, [j + 1, i], stats)
    draw_cb(arr, [], stats)


def quick_sort(arr, draw_cb, stats):
    def partition(lo, hi):
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            stats["comps"] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                stats["swaps"] += 1
            if stats["comps"] % 60 == 0:
                draw_cb(arr, [j, hi], stats)
                if DELAY: time.sleep(DELAY)
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        stats["swaps"] += 1
        draw_cb(arr, [i + 1, hi], stats)
        return i + 1

    def qsort(lo, hi):
        if lo < hi:
            p = partition(lo, hi)
            qsort(lo, p - 1)
            qsort(p + 1, hi)

    import sys
    sys.setrecursionlimit(10000)
    qsort(0, len(arr) - 1)
    draw_cb(arr, [], stats)


ALGORITHMS = [bubble_sort, selection_sort, insertion_sort, quick_sort]


class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmos de Ordenamiento")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.base_array = []
        self.threads    = []
        self.running    = False

        self._build_ui()
        self._reset()


    def _build_ui(self):
        # Título
        tk.Label(
            self.root, text="Visualización de Algoritmos de Ordenamiento",
            bg="#1e1e2e", fg="#cdd6f4", font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(14, 4))

        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        self.start_btn = tk.Button(
            btn_frame, text="▶  Iniciar", command=self._start,
            bg="#378ADD", fg="white", font=("Helvetica", 11, "bold"),
            relief="flat", padx=16, pady=6, cursor="hand2"
        )
        self.start_btn.pack(side="left", padx=6)

        tk.Button(
            btn_frame, text="↺  Reiniciar", command=self._reset,
            bg="#313244", fg="#cdd6f4", font=("Helvetica", 11),
            relief="flat", padx=16, pady=6, cursor="hand2"
        ).pack(side="left", padx=6)

        self.canvases   = []
        self.stat_vars  = []
        self.badge_vars = []
        self.prog_bars  = []

        for idx in range(4):
            row_pos = 2 + (idx // 2)
            col_pos = idx % 2

            frame = tk.Frame(self.root, bg="#313244", bd=0, padx=8, pady=8)
            frame.grid(row=row_pos, column=col_pos, padx=10, pady=6, sticky="nsew")

            hdr = tk.Frame(frame, bg="#313244")
            hdr.pack(fill="x")

            tk.Label(
                hdr, text=ALG_NAMES[idx],
                bg="#313244", fg=ALG_COLORS[idx],
                font=("Helvetica", 11, "bold")
            ).pack(side="left")

            badge_var = tk.StringVar(value="en espera")
            badge_lbl = tk.Label(
                hdr, textvariable=badge_var,
                bg="#45475a", fg="#cdd6f4",
                font=("Helvetica", 9), padx=6, pady=1
            )
            badge_lbl.pack(side="right")
            self.badge_vars.append((badge_var, badge_lbl))

            stat_var = tk.StringVar(value="Comps: 0   |   Swaps: 0")
            tk.Label(
                frame, textvariable=stat_var,
                bg="#313244", fg="#a6adc8",
                font=("Helvetica", 9)
            ).pack(anchor="w", pady=(2, 4))

            cv = tk.Canvas(
                frame, width=CANVAS_W, height=CANVAS_H,
                bg="#1e1e2e", highlightthickness=0
            )
            cv.pack()

            prog_bg = tk.Canvas(
                frame, width=CANVAS_W, height=4,
                bg="#45475a", highlightthickness=0
            )
            prog_bg.pack(pady=(4, 0))
            prog_fill = prog_bg.create_rectangle(0, 0, 0, 4, fill=ALG_COLORS[idx], width=0)

            self.canvases.append(cv)
            self.stat_vars.append(stat_var)
            self.prog_bars.append((prog_bg, prog_fill, CANVAS_W))

        leg_frame = tk.Frame(self.root, bg="#1e1e2e")
        leg_frame.grid(row=4, column=0, columnspan=2, pady=(4, 14))

        tk.Label(
            leg_frame, text="Valores  →  Colores:",
            bg="#1e1e2e", fg="#a6adc8", font=("Helvetica", 9)
        ).pack(side="left", padx=(0, 8))

        for i, color in enumerate(COLORS):
            box = tk.Canvas(leg_frame, width=18, height=18, bg="#1e1e2e", highlightthickness=0)
            box.create_rectangle(1, 1, 17, 17, fill=color, outline="")
            box.pack(side="left")
            tk.Label(
                leg_frame, text=str(i),
                bg="#1e1e2e", fg="#cdd6f4", font=("Helvetica", 9)
            ).pack(side="left", padx=(1, 6))


    def _reset(self):
        if self.running:
            return
        self.base_array = [random.randint(0, 9) for _ in range(N)]
        self.start_btn.config(state="normal", text="▶  Iniciar")
        for idx in range(4):
            self._draw(idx, self.base_array, [])
            self.stat_vars[idx].set("Comps: 0   |   Swaps: 0")
            bv, bl = self.badge_vars[idx]
            bv.set("en espera")
            bl.config(bg="#45475a", fg="#cdd6f4")
            pb, pf, w = self.prog_bars[idx]
            pb.coords(pf, 0, 0, 0, 4)

    def _start(self):
        if self.running:
            return
        self.running = True
        self.start_btn.config(state="disabled", text="Corriendo...")
        self.threads = []
        self._done_count = 0

        for idx in range(4):
            arr   = self.base_array.copy()
            stats = {"comps": 0, "swaps": 0}
            fn    = ALGORITHMS[idx]

            bv, bl = self.badge_vars[idx]
            bv.set("corriendo")
            bl.config(bg="#0c447c", fg="#b5d4f4")

            def make_cb(i, st):
                def cb(a, comparing, s):
                    self.root.after(0, self._update_panel, i, a, comparing, s)
                return cb

            t = threading.Thread(
                target=self._run_algo,
                args=(idx, fn, arr, stats, make_cb(idx, stats)),
                daemon=True
            )
            self.threads.append(t)

        for t in self.threads:
            t.start()

    def _run_algo(self, idx, fn, arr, stats, draw_cb):
        fn(arr, draw_cb, stats)
        self.root.after(0, self._mark_done, idx, arr, stats)

    def _update_panel(self, idx, arr, comparing, stats):
        self._draw(idx, arr, comparing)
        self.stat_vars[idx].set(
            f"Comps: {stats['comps']:,}   |   Swaps: {stats['swaps']:,}"
        )
        # Progreso estimado
        maxes = [N*N//2, N*N//2, N*N//2, int(N * 10 * 1.5)]
        pct   = min(stats["comps"] / maxes[idx], 0.99)
        pb, pf, w = self.prog_bars[idx]
        pb.coords(pf, 0, 0, int(w * pct), 4)

    def _mark_done(self, idx, arr, stats):
        self._draw(idx, arr, [])
        self.stat_vars[idx].set(
            f"Comps: {stats['comps']:,}   |   Swaps: {stats['swaps']:,}"
        )
        bv, bl = self.badge_vars[idx]
        bv.set("✓ listo")
        bl.config(bg="#3b6d11", fg="#c0dd97")
        pb, pf, w = self.prog_bars[idx]
        pb.coords(pf, 0, 0, w, 4)

        self._done_count += 1
        if self._done_count == 4:
            self.running = False
            self.start_btn.config(state="normal", text="▶  Iniciar")

    def _draw(self, idx, arr, comparing):
        cv = self.canvases[idx]
        cv.delete("all")
        bw = CANVAS_W / len(arr)
        for i, val in enumerate(arr):
            color  = "#ffffff" if i in comparing else COLORS[val]
            bar_h  = ((val + 1) / 10) * CANVAS_H
            x0 = i * bw
            x1 = x0 + max(bw - 0.3, 0.7)
            y0 = CANVAS_H - bar_h
            cv.create_rectangle(x0, y0, x1, CANVAS_H, fill=color, outline="")



if __name__ == "__main__":
    root = tk.Tk()
    app  = SortingApp(root)
    root.mainloop()
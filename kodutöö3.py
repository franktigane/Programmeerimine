import tkinter as tk
import math
import time

W, H    = 420, 480 #akna suurus
CX, CY  = 210, 220 # ketta keskpunkt (akna keskel)
R_DIAL  = 150   # ketta välisraadius
R_HOLES = 115   # augude kaugus keskmest
R_HOLE  = 16    # ühe augu raadius
R_INNER = 55    # keskaugu raadius
STOPPER = 330   # stopper-nurk kraadides
RETURN_TIME = 1.2  # sekundeid tagasipööramiseks

# number → augu nurk
HOLES = {"1":155,"2":172,"3":188,"4":205,"5":221,
         "6":238,"7":254,"8":271,"9":287,"0":304}

def angle_of(x, y):
    #Nurk keskmest, 0=üles, päripäeva.
    return (math.degrees(math.atan2(y - CY, x - CX)) + 90) % 360

class Dial:
    def __init__(self, root):
        self.root = root
        self.root.title("Kettatelefon")
        self.root.resizable(False, False)

        self.rot      = 0.0      # ketta praegune pöördenurk
        self.dragging = False    # kas hetkel kasutaja lohistab hiirega
        self.hole     = None     # Lohistatav auk
        self.drag_a0  = 0.0      # hiire nurk lohistuse alguses
        self.rot0     = 0.0      # ketta nurk lohistuse alguses
        self.digits   = []

        self.cv = tk.Canvas(root, width=W, height=H, bg="#1c1c1c", highlightthickness=0)
        self.cv.pack()

        # Displei
        self.disp = tk.StringVar()   #tkinteri üks muutuja
        tk.Label(root, textvariable=self.disp, font=("Courier", 22, "bold"),
                 fg="#00ff66", bg="#0a1a0a", width=16, anchor="w",
                 padx=8).pack(fill="x", padx=20, pady=(0, 4))

        # Nupud
        f = tk.Frame(root, bg="#1c1c1c")
        f.pack(fill="x", padx=20, pady=(0, 10))
        tk.Button(f, text=" Helista", font=("Courier", 12, "bold"),
                  fg="black", bg="#c0392b", relief="flat", padx=12, pady=6,
                  cursor="hand2", command=self.call).pack(side="left", expand=True, fill="x", padx=(0,4))
        tk.Button(f, text="✕ Kustuta", font=("Courier", 12, "bold"),
                  fg="black", bg="#444", relief="flat", padx=12, pady=6,
                  cursor="hand2", command=self.clear).pack(side="left", expand=True, fill="x")

        self.status = tk.StringVar()
        tk.Label(root, textvariable=self.status, font=("Courier", 11),
                 fg="#00ff66", bg="#1c1c1c").pack(pady=(0, 8))

        self.cv.bind("<ButtonPress-1>",  self.press)
        self.cv.bind("<B1-Motion>",      self.drag)
        self.cv.bind("<ButtonRelease-1>", self.release)
        self.draw()

    def hole_pos(self, label):
        #tagastab augu (x, y) praeguse rotatsiooni juures.
        a = math.radians(HOLES[label] + self.rot - 90)
        return CX + R_HOLES * math.cos(a), CY + R_HOLES * math.sin(a)

    def draw(self):
        c = self.cv
        c.delete("all")

        # Ketta taust
        c.create_oval(CX-R_DIAL, CY-R_DIAL, CX+R_DIAL, CY+R_DIAL,
                      fill="#c8a030", outline="#805010", width=3)
        c.create_oval(CX-R_DIAL+8, CY-R_DIAL+8, CX+R_DIAL-8, CY+R_DIAL-8,
                      fill="#d4b060", outline="")

        # Augud + numbrid
        for label in HOLES:
            hx, hy = self.hole_pos(label)
            c.create_oval(hx-R_HOLE-3, hy-R_HOLE-3, hx+R_HOLE+3, hy+R_HOLE+3,
                          fill="#a07020", outline="#604010", width=1)
            c.create_oval(hx-R_HOLE, hy-R_HOLE, hx+R_HOLE, hy+R_HOLE,
                          fill="#111", outline="#333")
            # number alla-poole auku
            nx = CX + (R_HOLES-28) * math.cos(math.radians(HOLES[label]+self.rot-90))
            ny = CY + (R_HOLES-28) * math.sin(math.radians(HOLES[label]+self.rot-90))
            c.create_text(nx, ny, text=label, font=("Georgia", 10, "bold"), fill="#3a2000")

        # Keskauk
        c.create_oval(CX-R_INNER, CY-R_INNER, CX+R_INNER, CY+R_INNER,
                      fill="#1c1c1c", outline="#805010", width=2)

        # Stopper (fikseeritud)
        sa = math.radians(STOPPER - 90)
        sx = CX + (R_DIAL - 10) * math.cos(sa)
        sy = CY + (R_DIAL - 10) * math.sin(sa)
        c.create_oval(sx-8, sy-8, sx+8, sy+8, fill="#c8a030", outline="#805010", width=2)
        c.create_oval(sx-3, sy-3, sx+3, sy+3, fill="#333")



    # HIIR
    def press(self, e):
        d = math.hypot(e.x-CX, e.y-CY)
        if not (R_INNER < d < R_DIAL):
            return
        for label in HOLES:
            hx, hy = self.hole_pos(label)
            if math.hypot(e.x-hx, e.y-hy) <= R_HOLE + 6:
                self.dragging = True
                self.hole     = label
                self.drag_a0  = angle_of(e.x, e.y)
                self.rot0     = self.rot
                return

    def drag(self, e):
        if not self.dragging:
            return
        delta   = (angle_of(e.x, e.y) - self.drag_a0 + 180) % 360 - 180
        max_rot = (STOPPER - HOLES[self.hole]) % 360
        self.rot = max(0.0, min(float(max_rot), self.rot0 + delta))
        self.draw()

    def release(self, e):
        if not self.dragging:
            return
        self.dragging = False
        max_rot = (STOPPER - HOLES[self.hole]) % 360
        if self.rot >= max_rot - 8:
            self.digits.append(self.hole)
            self.disp.set("".join(self.digits))
            self.status.set("")
        self.hole = None
        self._return_start()



    # TAGASIPÖÖRAMINE
    def _return_start(self):
        if self.rot < 1:
            self.rot = 0; self.draw(); return
        self._r0 = self.rot
        self._t0 = time.time()
        self._animate()

    def _animate(self):
        t = min((time.time() - self._t0) / RETURN_TIME, 1.0)
        self.rot = self._r0 * (1 - (1-t)**3)  # ease-out
        self.draw()
        if t < 1.0:
            self.root.after(16, self._animate)
        else:
            self.rot = 0; self.draw()

    # NUPUD
    def call(self):
        if not self.digits:
            self.status.set(" Vali esmalt number!"); return
        self.status.set(f" Helistan  {''.join(self.digits)} ...")

    def clear(self):
        self.digits = []
        self.disp.set("")
        self.status.set("")

root = tk.Tk()
Dial(root)
root.mainloop()

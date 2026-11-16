import psutil, speedtest, threading
import tkinter as tk

root = tk.Tk()
root.title(" Speeding net")



root.attributes("-topmost", True)

live = tk.Label(root, font=("Consolas", 16), padx=55, pady=25)
live.pack()

result = tk.Label(root, font=("Consolas", 12), text="Max speed: ...شوية استني")
result.pack(pady=5)

btn = tk.Button(root, text="speedtest", font=("Consolas", 15), padx=10, pady=5)
btn.pack(pady=10)

old = psutil.net_io_counters()

def update_live():
    global old
    new = psutil.net_io_counters()
    down = (new.bytes_recv - old.bytes_recv) * 8 / 1000000
    up = (new.bytes_sent - old.bytes_sent) * 8 / 1000000
    old = new
    live.config(text=f"DOWNLOAD ⬇ {down:.2f} Mbps\n UPLOAD ⬆ {up:.2f} Mbps")
    root.after(1000, update_live)

def run_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        d = st.download() / 1000000
        u = st.upload() / 1000000
        p = st.results.ping
        msg = f"Max⬇ {d:.1f} |⬆ {u:.1f} Mbps |Ping {p:.0f} ms"

    except Exception as e:

        msg = f"Error 400000: {e}"

        
    root.after(0, lambda: (result.config(text=msg), btn.config(state="normal")))

def start_test():
    btn.config(state="disabled")

    result.config(text="waiting for test.....")

    threading.Thread(target=run_test, daemon=True).start()

btn.config(command=start_test)
update_live()
root.mainloop()


img = tk.PhotoImage(file="icon.png")
root.iconphoto(True, img)
    


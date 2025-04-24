import tkinter as tk
from tkinter import messagebox
import math

def calculate_heat_transfer():
    try:
        t_h_in = float(entry_t_h_in.get())
        t_h_out = float(entry_t_h_out.get())
        t_c_in = float(entry_t_c_in.get())
        m_hot = float(entry_m_hot.get())
        cp_hot = float(entry_cp_hot.get())

        q = (m_hot / 3600) * cp_hot * (t_h_in - t_h_out)
        label_q.config(text=f"Heat Duty (Q): {q:.2f} kW")

        knows_tc_out = var_tc_out_known.get()

        if knows_tc_out:
            t_c_out = float(entry_t_c_out.get())
            m_cold = float(entry_m_cold.get())
        else:
            m_cold_known = var_m_cold_known.get()
            if m_cold_known:
                m_cold = float(entry_m_cold.get())
                cp_cold = float(entry_cp_cold.get())
                t_c_out = t_c_in + (q * 3600) / (m_cold * cp_cold)
                label_t_c_out.config(text=f"Estimated T_c_out: {t_c_out:.2f} °C")
            else:
                t_c_out = float(entry_t_c_out.get())
                cp_cold = float(entry_cp_cold.get())
                m_cold = (q * 3600) / (cp_cold * (t_c_out - t_c_in))
                label_m_cold.config(text=f"Estimated m_cold: {m_cold:.2f} kg/h")

        delta_t1 = t_h_in - t_c_out
        delta_t2 = t_h_out - t_c_in

        if abs(delta_t1 - delta_t2) < 1e-6:
            lmtd = delta_t1
        else:
            lmtd = (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)

        r = (t_h_in - t_h_out) / (t_c_out - t_c_in)
        s = (t_c_out - t_c_in) / (t_h_in - t_c_in)

        if r < 0.5 and s < 0.5:
            ft = 0.9
        elif r < 1.0 and s < 0.5:
            ft = 0.85
        elif r > 1.0 and s > 0.5:
            ft = 0.75
        else:
            ft = 0.8

        corrected_lmtd = ft * lmtd
        cp_cold = float(entry_cp_cold.get())
        mass_flow_cold_kg_s = q / (cp_cold * (t_c_out - t_c_in))

        u = float(entry_u.get())
        area = q * 1000 / (u * corrected_lmtd)

        outer_dia = float(entry_dia.get())
        length = float(entry_length.get())
        area_of_one_tube = 3.1416 * outer_dia * length
        no_of_tubes = area / area_of_one_tube

        label_results.config(text=f"Corrected LMTD: {corrected_lmtd:.2f} K\n"
                                      f"Required cold mass flow rate: {mass_flow_cold_kg_s:.2f} kg/s\n"
                                      f"Required Area: {area:.2f} m²\n"
                                      f"No. of Tubes: {math.ceil(no_of_tubes)}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Heat Exchanger Calculator")

entries = []

labels = ["Hot fluid inlet temp (°C)", "Hot fluid outlet temp (°C)", "Cold fluid inlet temp (°C)",
          "Hot fluid mass flow rate (kg/h)", "Hot fluid specific heat (kJ/kg·K)",
          "Cold fluid outlet temp (°C)", "Cold fluid mass flow rate (kg/h)",
          "Cold fluid specific heat (kJ/kg·K)", "Overall heat transfer coefficient U (W/m²·K)",
          "Outer diameter (m)", "Tube length (m)"]

entries_vars = []

for i, text in enumerate(labels):
    label = tk.Label(root, text=text)
    label.grid(row=i, column=0, sticky='w')
    var = tk.StringVar()
    entry = tk.Entry(root, textvariable=var)
    entry.grid(row=i, column=1)
    entries_vars.append(var)

entry_t_h_in = entries_vars[0]
entry_t_h_out = entries_vars[1]
entry_t_c_in = entries_vars[2]
entry_m_hot = entries_vars[3]
entry_cp_hot = entries_vars[4]
entry_t_c_out = entries_vars[5]
entry_m_cold = entries_vars[6]
entry_cp_cold = entries_vars[7]
entry_u = entries_vars[8]
entry_dia = entries_vars[9]
entry_length = entries_vars[10]

var_tc_out_known = tk.BooleanVar()
check_tc_out_known = tk.Checkbutton(root, text="Know cold fluid outlet temp?", variable=var_tc_out_known)
check_tc_out_known.grid(row=12, column=0, columnspan=2, sticky='w')

var_m_cold_known = tk.BooleanVar()
check_m_cold_known = tk.Checkbutton(root, text="Know cold fluid mass flow rate?", variable=var_m_cold_known)
check_m_cold_known.grid(row=13, column=0, columnspan=2, sticky='w')

btn_calc = tk.Button(root, text="Calculate", command=calculate_heat_transfer)
btn_calc.grid(row=14, column=0, columnspan=2, pady=10)

label_q = tk.Label(root, text="")
label_q.grid(row=15, column=0, columnspan=2)

label_t_c_out = tk.Label(root, text="")
label_t_c_out.grid(row=16, column=0, columnspan=2)

label_m_cold = tk.Label(root, text="")
label_m_cold.grid(row=17, column=0, columnspan=2)

label_results = tk.Label(root, text="")
label_results.grid(row=18, column=0, columnspan=2)

root.mainloop()


import random
import tkinter as tk
from tkinter import ttk


def arvuta_kalorid(vanus, sugu, kaal, pikkus, aktiivsus, eesmärk):
    
    # Peatab koodi ettearvamatutes olukordades.
    if kaal > 99999:
        return """Sinu kaal on suurem, kui minu lootused elus.
Kas Tahad, et ma helistan jõusaali treenerile, et aidata sul seda langetada?"""
        
    if kaal < 1:
        return "Liiga väike number kaalus."
        
    if pikkus > 99999:
        arv_pikkus = pikkus / 100
        return "Teie pikkus: " + str(arv_pikkus) + " m. Kas olete mõõtnud oma pikkust või üritanud mõõta Munamäe kõrgust?"
        
    if pikkus < 1:
        return "Olete liiga lühike."
        
        
    if vanus > 999:
        return "Teie vanus on nii suur, et isegi kalendri lehed hakkavad kartma!"
        
    if vanus < 1:
        return "Olete liiga noor selle programmi kasutuseks."
    
    # Arvutab BMR vastavalt soole
    if sugu == "mees":
        bmr = 88.36 + (13.4 * kaal) + (4.8 * pikkus) - (5.7 * vanus)
    elif sugu == "naine":
        bmr = 447.6 + (9.2 * kaal) + (3.1 * pikkus) - (4.3 * vanus)
    else:
        return "Sugu peab olema 'mees' või 'naine'."

    # Määrab aktiivsuse
    if aktiivsus == "istuv":
        aktiivsustegur = 1.2
    elif aktiivsus == "väike":
        aktiivsustegur = 1.375
    elif aktiivsus == "mõõdukas":
        aktiivsustegur = 1.55
    elif aktiivsus == "kõrge":
        aktiivsustegur = 1.725
    elif aktiivsus == "väga kõrge":
        aktiivsustegur = 1.9
    else:
        return "Aktiivsuse tase peab olema 'istuv', 'väike', 'mõõdukas', 'kõrge' või 'väga kõrge'."

    kalorid = bmr * aktiivsustegur

    if eesmärk == "kaalulangus":
        kalorid -= 500
    elif eesmärk == "kaalutõus":
        kalorid += 500
    elif eesmärk == "kaalu säilitamine":
        kalorid -= 0
    else:
        return "Eesmärk peab olema 'kaalulangus', 'kaalutõus' või 'kaalu säilitamine'."
    

    valgud_kalorid = kalorid * 0.25
    rasvad_kalorid = kalorid * 0.3
    süsivesikud_kalorid = kalorid * 0.45

    return kalorid, valgud_kalorid, rasvad_kalorid, süsivesikud_kalorid
    



def planeeri_toitumine(kalorid):
    # Arvutab toiduained toitumiskavasse
    toiduained = {}
    with open("toidud.txt", "r", encoding="utf-8") as f:
        for rida in f:
            toit, kalorsus = rida.strip().split("-")
            toiduained[toit] = int(kalorsus)

    toitumiskava = []
    while kalorid > 0:
        toit = random.choice(list(toiduained.keys()))
        kogus = round(kalorid / toiduained[toit] * 100, 2)
        if kogus > 100:
            kogus = 100
        toitumiskava.append((toit, kogus))
        kalorid -= toiduained[toit] * kogus / 100

    return toitumiskava


def kuva_graafika():
    # Kuvab graafilise kasutajaliidese.

    def arvuta():
        # Arvutab valgud, rasvad ja süsivesikud
        try:
            vanus = int(vanus_entry.get())
            sugu = sugu_combo.get()
            kaal = float(kaal_entry.get())
            pikkus = float(pikkus_entry.get())
            aktiivsus = aktiivsus_combo.get()
            eesmärk = eesmärk_combo.get()

            tulemused = arvuta_kalorid(vanus, sugu, kaal, pikkus, aktiivsus, eesmärk)

            if isinstance(tulemused, str):
                tulemus_label.config(text=tulemused)
            else:
                kalorid, valgud_kalorid, rasvad_kalorid, süsivesikud_kalorid = tulemused
                tulemus_label.config(
                    text=f"Teie päevane kalorikulu on: {kalorid:.2f} kcal\n"
                    f"Valgud: {valgud_kalorid:.2f} kcal\n"
                    f"Rasvad: {rasvad_kalorid:.2f} kcal\n"
                    f"Süsivesikud: {süsivesikud_kalorid:.2f} kcal"
                )

                # Toitumiskava genereerimine ja kuvamine
                if toitumis_kava_var.get():
                    toitumiskava = planeeri_toitumine(kalorid)
                    toitumiskava_text.config(state="normal")
                    toitumiskava_text.delete("1.0", tk.END)
                    toitumiskava_text.insert(tk.END, "Teie toitumiskava:\n")
                    for toit, kogus in toitumiskava:
                        toitumiskava_text.insert(tk.END, f"{toit}: {kogus:.2f} g\n")
                    toitumiskava_text.config(state="disabled")
                    toitumiskava_text.grid() # tekst nähtavaks
                    
                else:
                    toitumiskava_text.grid_remove() # teksti ära kustutamine

        except ValueError:
            tulemus_label.config(text="Vigased andmed!")

    aken = tk.Tk()
    aken.title("Kalorite kalkulaator")

    # Vanus
    vanus_label = ttk.Label(aken, text="Vanus (aastad):")
    vanus_label.grid(row=0, column=0, padx=5, pady=5)
    vanus_entry = ttk.Entry(aken)
    vanus_entry.grid(row=0, column=1, padx=5, pady=5)

    # Sugu
    sugu_label = ttk.Label(aken, text="Sugu:")
    sugu_label.grid(row=1, column=0, padx=5, pady=5)
    sugu_combo = ttk.Combobox(aken, values=["mees", "naine"], state="readonly")
    sugu_combo.grid(row=1, column=1, padx=5, pady=5)

    # Kaal
    kaal_label = ttk.Label(aken, text="Kaal (kg):")
    kaal_label.grid(row=2, column=0, padx=5, pady=5)
    kaal_entry = ttk.Entry(aken)
    kaal_entry.grid(row=2, column=1, padx=5, pady=5)

    # Pikkus
    pikkus_label = ttk.Label(aken, text="Pikkus (cm):")
    pikkus_label.grid(row=3, column=0, padx=5, pady=5)
    pikkus_entry = ttk.Entry(aken)
    pikkus_entry.grid(row=3, column=1, padx=5, pady=5)

    # Aktiivsus
    aktiivsus_label = ttk.Label(aken, text="Aktiivsus:")
    aktiivsus_label.grid(row=4, column=0, padx=5, pady=5)
    aktiivsus_combo = ttk.Combobox(
        aken, values=["istuv", "väike", "mõõdukas", "kõrge", "väga kõrge"],state="readonly"
    )
    aktiivsus_combo.grid(row=4, column=1, padx=5, pady=5)

    # Eesmärk
    eesmärk_label = ttk.Label(aken, text="Eesmärk:")
    eesmärk_label.grid(row=5, column=0, padx=5, pady=5)
    eesmärk_combo = ttk.Combobox(
        aken, values=["kaalulangus", "kaalutõus", "kaalu säilitamine"], state="readonly"
    )
    eesmärk_combo.grid(row=5, column=1, padx=5, pady=5)

    # Toitumiskava valik
    toitumis_kava_label = ttk.Label(aken, text="Kas soovid toitumiskava?:")
    toitumis_kava_label.grid(row=6, column=0, padx=5, pady=5)
    toitumis_kava_var = tk.BooleanVar()
    toitumis_kava_check = ttk.Checkbutton(aken, variable=toitumis_kava_var, text="jah")
    toitumis_kava_check.grid(row=6, column=1, padx=5, pady=5)

    #Arvuta nupp
    arvuta_nupp = ttk.Button(aken, text="Arvuta", command=arvuta)
    arvuta_nupp.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    # Tulemus
    tulemus_label = ttk.Label(aken, text="")
    tulemus_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    # Toitumiskava kuvamine
    toitumiskava_text = tk.Text(aken, state="disabled", font=("Calibri", 10))
    
    # Alguses on tekst peidetud
    toitumiskava_text.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
    toitumiskava_text.grid_remove() 

    aken.mainloop()


if __name__ == "__main__":
    kuva_graafika()

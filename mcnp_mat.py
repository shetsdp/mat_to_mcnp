import tkinter as tk
from tkinter import messagebox
import re
from collections import defaultdict

NATURAL_ABUNDANCE = {
"H": {1: 99.9885, 2: 0.0115},
"He": {3: 0.000137, 4: 99.999863},
"Li": {6: 7.59, 7: 92.41},
"Be": {9: 100},
"B": {10: 19.9, 11: 80.1},
"C": {12: 98.93, 13: 1.07},
"N": {14: 99.636, 15: 0.364},
"O": {16: 99.757, 17: 0.243},
"F": {19: 100},
"Ne": {20: 90.48, 21: 0.27, 22: 9.25},
"Na": {23: 100},
"Mg": {24: 78.99, 25: 10.00, 26: 11.01},
"Al": {27: 100},
"Si": {28: 92.23, 29: 4.67, 30: 3.10},
"P": {31: 100},
"S": {32: 94.99, 33: 0.75, 34: 4.25, 36: 0.01},
"Cl": {35: 75.78, 37: 24.22},
"Ar": {36: 0.3365, 38: 0.0632, 40: 99.6003},
"K": {39: 93.2581, 40: 0.0117, 41: 6.7302},
"Ca": {40: 96.941, 42: 0.647, 43: 0.135, 44: 2.086, 46: 0.004, 48: 0.187},
"Sc": {45: 100},
"Ti": {46: 8.25, 47: 7.44, 48: 73.72, 49: 5.41, 50: 5.18},
"V": {50: 0.25, 51: 99.75},
"Cr": {50: 4.345, 52: 83.789, 53: 9.501, 54: 2.365},
"Mn": {55: 100},
"Fe": {54: 5.845, 56: 91.754, 57: 2.119, 58: 0.282},
"Co": {59: 100},
"Ni": {58: 68.077, 60: 26.223, 61: 1.140, 62: 3.635, 64: 0.926},
"Cu": {63: 69.15, 65: 30.85},
"Zn": {64: 48.63, 66: 27.90, 67: 4.10, 68: 18.75, 70: 0.62},
"Ga": {69: 60.108, 71: 39.892},
"Ge": {70: 20.84, 72: 27.54, 73: 7.73, 74: 36.28, 76: 7.61},
"As": {75: 100},
"Se": {74: 0.89, 76: 9.37, 77: 7.63, 78: 23.77, 80: 49.61, 82: 8.73},
"Br": {79: 50.69, 81: 49.31},
"Kr": {78: 0.35, 80: 2.25, 82: 11.6, 83: 11.5, 84: 57.0, 86: 17.3},
"Rb": {85: 72.17, 87: 27.83},
"Sr": {84: 0.56, 86: 9.86, 87: 7.00, 88: 82.58},
"Y": {89: 100},
"Zr": {90: 51.45, 91: 11.22, 92: 17.15, 94: 17.38, 96: 2.80},
"Nb": {93: 100},
"Mo": {92: 14.84, 94: 9.25, 95: 15.92, 96: 16.68, 97: 9.55, 98: 24.13, 100: 9.63},
"Tc": {99: 100},
"Ru": {96: 5.54, 98: 1.87, 99: 12.76, 100: 12.60, 101: 17.06, 102: 31.55, 104: 18.62},
"Rh": {103: 100},
"Pd": {102: 1.02, 104: 11.14, 105: 22.33, 106: 27.33, 108: 26.46, 110: 11.72},
"Ag": {107: 51.839, 109: 48.161},
"Cd": {106: 1.25, 108: 0.89, 110: 12.49, 111: 12.80, 112: 24.13, 113: 12.22, 114: 28.73, 116: 7.49},
"In": {113: 4.29, 115: 95.71},
"Sn": {112: 0.97, 114: 0.66, 115: 0.34, 116: 14.54, 117: 7.68, 118: 24.22, 119: 8.59, 120: 32.58, 122: 4.63, 124: 5.79},
"Sb": {121: 57.21, 123: 42.79},
"Te": {120: 0.09, 122: 2.55, 123: 0.89, 124: 4.74, 125: 7.07, 126: 18.84, 128: 31.74, 130: 34.08},
"I": {127: 100},
"Xe": {124: 0.095, 126: 0.089, 128: 1.92, 129: 26.44, 130: 4.08, 131: 21.18, 132: 26.89, 134: 10.44, 136: 8.87},
"Cs": {133: 100},
"Ba": {130: 0.106, 132: 0.101, 134: 2.417, 135: 6.592, 136: 7.854, 137: 11.232, 138: 71.698},
"La": {138: 0.09, 139: 99.91},
"Ce": {136: 0.19, 138: 0.25, 140: 88.45, 142: 11.11},
"Pr": {141: 100},
"Nd": {142: 27.2, 143: 12.2, 144: 23.8, 145: 8.3, 146: 17.2, 148: 5.7, 150: 5.6},
"Pm": {147: 100},
"Sm": {144: 3.1, 147: 15.0, 148: 11.3, 149: 13.8, 150: 7.4, 152: 26.7, 154: 22.7},
"Eu": {151: 47.8, 153: 52.2},
"Gd": {152: 0.20, 154: 2.18, 155: 14.80, 156: 20.47, 157: 15.65, 158: 24.84, 160: 21.86},
"Tb": {159: 100},
"Dy": {156: 0.06, 158: 0.10, 160: 2.34, 161: 18.91, 162: 25.51, 163: 24.90, 164: 28.18},
"Ho": {165: 100},
"Er": {162: 0.14, 164: 1.61, 166: 33.61, 167: 22.95, 168: 26.78, 170: 14.93},
"Tm": {169: 100},
"Yb": {168: 0.13, 170: 3.05, 171: 14.3, 172: 21.9, 173: 16.12, 174: 31.8, 176: 12.7},
"Lu": {175: 97.41, 176: 2.59},
"Hf": {174: 0.16, 176: 5.26, 177: 18.6, 178: 27.28, 179: 13.62, 180: 35.08},
"Ta": {180: 0.012, 181: 99.988},
"W": {180: 0.12, 182: 26.50, 183: 14.31, 184: 30.64, 186: 28.43},
"Re": {185: 37.4, 187: 62.6},
"Os": {184: 0.02, 186: 1.59, 187: 1.96, 188: 13.24, 189: 16.15, 190: 26.26, 192: 40.78},
"Ir": {191: 37.3, 193: 62.7},
"Pt": {190: 0.014, 192: 0.782, 194: 32.967, 195: 33.832, 196: 25.242, 198: 7.163},
"Au": {197: 100},
"Hg": {196: 0.15, 198: 10.04, 199: 16.94, 200: 23.14, 201: 13.17, 202: 29.74, 204: 6.82},
"Tl": {203: 29.524, 205: 70.476},
"Pb": {204: 1.4, 206: 24.1, 207: 22.1, 208: 52.4},
"Bi": {209: 100},
"Po": {209: 100},
"At": {210: 100},
"Rn": {222: 100},
"Fr": {223: 100},
"Ra": {226: 100},
"Ac": {227: 100},
"Th": {232: 100},
"Pa": {231: 100},
"U": {234: 0.0055, 235: 0.7200, 238: 99.2745}
}
# Build Z lookup for the elements we support
ELEMENT_Z = {
"H": 1,  "He": 2,
"Li": 3, "Be": 4, "B": 5,  "C": 6,  "N": 7,  "O": 8,  "F": 9,  "Ne": 10,
"Na": 11,"Mg": 12,"Al": 13,"Si": 14,"P": 15, "S": 16, "Cl": 17,"Ar": 18,
"K": 19, "Ca": 20,"Sc": 21,"Ti": 22,"V": 23, "Cr": 24,"Mn": 25,"Fe": 26,
"Co": 27,"Ni": 28,"Cu": 29,"Zn": 30,"Ga": 31,"Ge": 32,"As": 33,"Se": 34,
"Br": 35,"Kr": 36,"Rb": 37,"Sr": 38,"Y": 39, "Zr": 40,"Nb": 41,"Mo": 42,
"Tc": 43,"Ru": 44,"Rh": 45,"Pd": 46,"Ag": 47,"Cd": 48,"In": 49,"Sn": 50,
"Sb": 51,"Te": 52,"I": 53, "Xe": 54,"Cs": 55,"Ba": 56,"La": 57,"Ce": 58,
"Pr": 59,"Nd": 60,"Pm": 61,"Sm": 62,"Eu": 63,"Gd": 64,"Tb": 65,"Dy": 66,
"Ho": 67,"Er": 68,"Tm": 69,"Yb": 70,"Lu": 71,"Hf": 72,"Ta": 73,"W": 74,
"Re": 75,"Os": 76,"Ir": 77,"Pt": 78,"Au": 79,"Hg": 80,"Tl": 81,"Pb": 82,
"Bi": 83,"Po": 84,"At": 85,"Rn": 86,"Fr": 87,"Ra": 88,"Ac": 89,"Th": 90,
"Pa": 91,"U": 92
}

SUBSCRIPT_MAP = str.maketrans("₀₁₂₃₄₅₆₇₈₉₊₋", "0123456789+-")

# -----------------------------
# LOGIC (UNCHANGED)
# -----------------------------
def normalize_text(s):
    return s.translate(SUBSCRIPT_MAP).replace(" ", "")

def parse_formula(formula):
    tokens = re.findall(r"[A-Z][a-z]?|\d+|[()]", formula)
    stack = [defaultdict(float)]
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == "(":
            stack.append(defaultdict(float))
        elif tok == ")":
            group = stack.pop()
            mult = 1.0
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                mult = float(tokens[i + 1]); i += 1
            for el, cnt in group.items():
                stack[-1][el] += cnt * mult
        elif re.match(r"[A-Z][a-z]?", tok):
            el = tok
            cnt = 1.0
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                cnt = float(tokens[i + 1]); i += 1
            stack[-1][el] += cnt
        i += 1
    return dict(stack[0])

def parse_recipe(recipe):
    recipe = normalize_text(recipe)
    parts = recipe.split("-")
    out = []
    for p in parts:
        m = re.fullmatch(r"(\d+(?:\.\d+)?)([A-Za-z][A-Za-z0-9()]*?)", p)
        if not m:
            raise ValueError(f"Cannot parse: {p}")
        out.append((float(m.group(1)), m.group(2)))
    return out

def recipe_to_element_atom_fractions(recipe):
    components = parse_recipe(recipe)
    element_moles = defaultdict(float)
    for mol_percent, formula in components:
        comp = parse_formula(formula)
        for el, n in comp.items():
            element_moles[el] += mol_percent * n
    total = sum(element_moles.values())
    return {el: moles / total for el, moles in element_moles.items()}

def element_atom_fractions_to_isotopes(element_fracs):
    iso_moles = defaultdict(float)
    for el, x_el in element_fracs.items():
        abund = NATURAL_ABUNDANCE[el]
        z = ELEMENT_Z[el]
        total_ab = sum(abund.values())
        for A, p in abund.items():
            zaid = z*1000 + A
            iso_moles[zaid] += x_el * (p/total_ab)
    total = sum(iso_moles.values())
    return {k: v/total for k,v in iso_moles.items()}

def build_mcnp_material_card(recipe, suffix):
    elem = recipe_to_element_atom_fractions(recipe)
    iso = element_atom_fractions_to_isotopes(elem)
    lines = ["m1"]
    for zaid in sorted(iso):
        lines.append(f"     {zaid}{suffix} {iso[zaid]:.8e}")
    return "\n".join(lines)

# -----------------------------
# GUI
# -----------------------------
def generate():
    try:
        recipe = entry_recipe.get()
        suffix = entry_suffix.get()
        result = build_mcnp_material_card(recipe, suffix)

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def copy_output():
    root.clipboard_clear()
    root.clipboard_append(text_output.get(1.0, tk.END))
    messagebox.showinfo("Copied", "Copied to clipboard!")

root = tk.Tk()
root.title("MCNP Material Generator")

tk.Label(root, text="Recipe:").pack()
entry_recipe = tk.Entry(root, width=60)
entry_recipe.pack()
entry_recipe.insert(0, "12B2O3-16SiO2-4Gd2O3-36TeO2-12Bi2O3-12ZnO-8BaO")

tk.Label(root, text="Suffix (.72c):").pack()
entry_suffix = tk.Entry(root, width=20)
entry_suffix.pack()
entry_suffix.insert(0, ".72c")

tk.Button(root, text="Generate", command=generate).pack(pady=5)
tk.Button(root, text="Copy", command=copy_output).pack(pady=5)

text_output = tk.Text(root, height=20, width=80)
text_output.pack()

root.mainloop()
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import random
import json
import difflib
import string  # Necesar pentru noua funcție de normalizare
from datetime import datetime

# --- BAZA DE CUNOȘTINȚE (TIP 1) - BAZATĂ PE CURSURILE S2, S3, S4 ---
# Această variabilă înlocuiește toate versiunile anterioare.

KB_TYPE_1_SCENARIOS = [

    # --- Scenarii din Cursul 2 (Săptămâna 2: Căutare Neinformată) ---

    {
        'id': 'bfs-optimal',
        'problem': 'găsirea unui drum într-un graf',
        'instance': 'o instanță unde se dorește garantarea celei mai scurte căi (soluția optimă)',
        'goal': 'ce strategie neinformată garantează găsirea soluției optime? [Curs S2, pg. 23, 27]',
        'answers': [
            'bfs (breadth first search)',
            'uniform cost search',
            'căutare pe lățime'
        ],
        'wrong_keywords': [
            'dfs (depth first search)', 'backtracking', 'random'
        ]
    },
    {
        'id': 'dfs-loops-problem',
        'problem': 'găsirea unui drum într-un graf',
        'instance': 'o instanță de graf care conține cicluri (bucle)',
        'goal': 'ce strategie neinformată riscă să intre într-o buclă infinită și să nu se termine? [Curs S2, pg. 24]',
        'answers': [
            'dfs (depth first search)',
            'căutare în adâncime'
        ],
        'wrong_keywords': [
            'bfs (breadth first search)', 'backtracking', 'ids (iterative deepening)'
        ]
    },
    {
        'id': 'backtracking-vs-dfs-memory',
        'problem': 'rezolvarea unei probleme cu un spațiu al stărilor foarte mare',
        'instance': 'o instanță unde memoria este o constrângere critică',
        'goal': 'ce strategie (conform cursului) este diferită de DFS și *nu* necesită memorarea stărilor vizitate? [Curs S2, pg. 25]',
        'answers': [
            'backtracking'
        ],
        'wrong_keywords': [
            'dfs (depth first search)', 'bfs (breadth first search)', 'uniform cost'
        ]
    },
    {
        'id': 'ids-solves-dfs',
        'problem': 'găsirea unui drum într-un graf',
        'instance': 'un graf cu adâncime mare sau necunoscută, posibil cu cicluri',
        'goal': 'ce strategie rezolvă problema căilor infinite a lui DFS, fără a folosi memoria masivă cerută de BFS? [Curs S2, pg. 24]',
        'answers': [
            'ids (iterative deepening search)',
            'căutare iterativă în adâncime'
        ],
        'wrong_keywords': [
            'dfs (depth first search)', 'backtracking', 'bfs'
        ]
    },

    # --- Scenarii din Cursul 3 (Săptămâna 3: Căutare Informată) ---

    {
        'id': 'a-star-optimal',
        'problem': 'găsirea unui drum într-un graf',
        'instance': 'o instanță unde se dorește garantarea celei mai scurte căi (soluția optimă), dar avem și o euristică',
        'goal': 'ce strategie informată găsește *întotdeauna* soluția optimă (dacă euristica este admisibilă)? [Curs S3, pg. 18, 19]',
        'answers': [
            'a*',
            'a star',
            'a-star'
        ],
        'wrong_keywords': [
            'greedy', 'best-first', 'hillclimbing', 'bfs'
        ]
    },
    {
        'id': 'greedy-fast-not-optimal',
        'problem': 'găsirea unui drum într-un graf',
        'instance': 'o instanță unde se dorește găsirea *rapidă* a unei soluții, chiar dacă nu e cea mai bună',
        'goal': 'ce strategie informată alege starea "cea mai apropiată de scop" conform euristicii, dar *nu* garantează optimalitatea? [Curs S3, pg. 9, 10]',
        'answers': [
            'greedy',
            'best-first',
            'greedy best-first'
        ],
        'wrong_keywords': [
            'a*', 'a star', 'bfs', 'uniform cost'
        ]
    },
    {
        'id': 'hillclimbing-local-optimum',
        'problem': 'optimizarea unei funcții euristice',
        'instance': 'un spațiu al stărilor cu multe "capcane" (maxime locale)',
        'goal': 'ce strategie rapidă riscă să se blocheze într-un "local optimum" și să nu găsească soluția globală? [Curs S3, pg. 12]',
        'answers': [
            'hillclimbing',
            'hill climbing'
        ],
        'wrong_keywords': [
            'simulated annealing', 'a*', 'greedy', 'bfs'
        ]
    },
    {
        'id': 'simulated-annealing-solves-hillclimbing',
        'problem': 'optimizarea unei funcții euristice',
        'instance': 'un spațiu al stărilor cu multe "capcane" (maxime locale)',
        'goal': 'ce variantă a Hillclimbing-ului este concepută special pentru a *evita* blocarea în maximele locale? [Curs S3, pg. 14]',
        'answers': [
            'simulated annealing',
            'recoacere simulată'
        ],
        'wrong_keywords': [
            'hillclimbing', 'greedy', 'a*', 'backtracking'
        ]
    },

    # --- Scenarii din Cursul 4 (CSP) ---

    {
        'id': 'csp-mrv-heuristic',
        'problem': 'rezolvarea unei probleme CSP (ex: colorarea hărții)',
        'instance': 'în timpul rulării algoritmului Backtracking, trebuie să alegem următoarea variabilă',
        'goal': 'care e euristica "fail-first" (alege variabila cu cele mai puține valori legale rămase)? [Curs CSP, pg. 25]',
        'answers': [
            'mrv (minimum-remaining-values)',
            'minimum remaining values',
            'variabila cea mai constrânsă'
        ],
        'wrong_keywords': [
            'lcv (least-constraining-value)', 'forward checking', 'ac-3'
        ]
    },
    {
        'id': 'csp-lcv-heuristic',
        'problem': 'rezolvarea unei probleme CSP (ex: colorarea hărții)',
        'instance': 'în timpul rulării Backtracking, am ales o variabilă (ex: Q) și trebuie să alegem ce *valoare* să încercăm prima',
        'goal': 'care e euristica ce alege valoarea care *elimină cele mai puține* opțiuni pentru vecini? [Curs CSP, pg. 26]',
        'answers': [
            'lcv (least-constraining-value)',
            'least constraining value',
            'valoarea cea mai puțin constrânsă'
        ],
        'wrong_keywords': [
            'mrv (minimum-remaining-values)', 'forward checking', 'ac-3'
        ]
    },
    {
        'id': 'csp-fc-vs-ac3',
        'problem': 'rezolvarea unei probleme CSP (ex: colorarea hărții)',
        'instance': 'după o asignare (ex: WA=red), trebuie să detectăm eșecurile viitoare',
        'goal': 'ce tehnică de propagare (mai puternică decât Forward Checking) verifică consistența *între* variabilele neasignate? [Curs CSP, pg. 35, 39]',
        'answers': [
            'arc consistency',
            'ac-3',
            'consistența arcelor'
        ],
        'wrong_keywords': [
            'forward checking', 'mrv', 'lcv', 'backtracking'
        ]
    },
    {
        'id': 'csp-min-conflicts',
        'problem': 'rezolvarea unei probleme CSP mari (ex: n-Queens)',
        'instance': 'folosind o abordare de Căutare Locală cu o stare completă (toate variabilele asignate)',
        'goal': 'care e euristica ce alege o variabilă în conflict și o mută în poziția care *încalcă cele mai puține* constrângeri? [Curs CSP, pg. 54]',
        'answers': [
            'min-conflicts',
            'minimum conflicts'
        ],
        'wrong_keywords': [
            'backtracking', 'mrv', 'lcv', 'forward checking', 'hillclimbing'
        ]
    }
]
LOG_FILE = 'log_interactions.json'


# --- Funcția de Normalizare a Textului ---

def normalize_text(s):
    """
    Convertește textul la litere mici, elimină punctuația și spațiile multiple.
    """
    s = s.lower()
    s = s.translate(str.maketrans('', '', string.punctuation))
    return ' '.join(s.strip().split())


# --- NOUA Funcție de Evaluare "Pseudo-Semantică" (Non-AI) ---

# ÎNLOCUIEȘTE ACEASTĂ FUNCȚIE

def evaluate_strategy_answer(user_answer, correct_answers_list, wrong_keywords_list, similarity_threshold=0.6):
    """
    Evaluează un răspuns text folosind o logică bazată pe liste (albă/neagră).
    FĂRĂ a folosi un agent AI.
    """
    ua_norm = normalize_text(user_answer)
    if not ua_norm:
        return 0  # Răspuns gol

    user_words = set(ua_norm.split())

    # --- Pasul 1: Verificăm Lista Neagră (Greșeli) ---
    wrong_keywords = set()
    for kw_list in wrong_keywords_list:
        for word in normalize_text(kw_list).split():
            if len(word) > 3: wrong_keywords.add(word)

    found_wrong_keyword = False
    for kw in user_words:
        if kw in wrong_keywords:
            found_wrong_keyword = True
            break

    if found_wrong_keyword:
        # Penalizare imediată! Ai menționat un concept greșit.
        return 0

    # --- Pasul 2: Verificăm Lista Albă (Corect) ---
    # (Doar dacă nu s-a găsit nicio greșeală)
    correct_keywords = set()
    for ans in correct_answers_list:
        for word in normalize_text(ans).split():
            if len(word) > 3: correct_keywords.add(word)

    found_correct_keyword = False
    for kw in user_words:
        if kw in correct_keywords:
            found_correct_keyword = True
            break

    if found_correct_keyword:
        # Ai menționat un concept corect și niciunul greșit.
        return 100

    # --- Pasul 3: Fallback (Typos) ---
    # (Doar dacă nu s-a găsit niciun cuvânt cheie, nici bun, nici rău)
    best_ratio = 0.0
    for ans in correct_answers_list:
        ans_norm = normalize_text(ans)
        ratio = difflib.SequenceMatcher(None, ua_norm, ans_norm).ratio()
        if ratio > best_ratio:
            best_ratio = ratio

    if best_ratio >= similarity_threshold:
        return int(best_ratio * 100)  # Prinde "backtraking"
    else:
        return 0  # Răspuns necunoscut și nesimilar (ex: "nu stiu")
# ----- Functii pentru log (din codul tău original) -----

def load_log():
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_log(log):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


# ----- Aplicatie GUI (Structura ta originală) -----
# ---
# Aici ar trebui să fie funcțiile `normalize_text`, `evaluate_strategy_answer`,
# `load_log`, `save_log` și variabila KB_TYPE_1_SCENARIOS
# ---

# --- CLASA SmarTestApp ACTUALIZATĂ ---

class SmarTestApp:
    def __init__(self, master):
        self.master = master
        master.title('SmarTest - L6 (Tipul 1: Bazat pe Instanțe)')
        master.geometry('800x520')

        # Frame întrebări
        self.q_frame = tk.Frame(master)
        self.q_frame.pack(padx=10, pady=8, fill='x')

        self.question_label = tk.Label(self.q_frame, text='Întrebare:', font=('Arial', 14, 'bold'))
        self.question_label.pack(anchor='w')

        self.question_text = tk.Label(self.q_frame, text='', font=('Arial', 12), wraplength=760, justify='left')
        self.question_text.pack(anchor='w', pady=(4, 0))

        # Frame raspuns
        self.a_frame = tk.Frame(master)
        self.a_frame.pack(padx=10, pady=8, fill='both', expand=True)

        self.answer_label = tk.Label(self.a_frame, text='Răspunsul tău:', font=('Arial', 12))
        self.answer_label.pack(anchor='w')

        self.answer_entry = scrolledtext.ScrolledText(self.a_frame, height=6, wrap='word', font=('Arial', 11))
        self.answer_entry.pack(fill='x', pady=(4, 10))

        # Butoane
        self.btn_frame = tk.Frame(master)
        self.btn_frame.pack(padx=10, pady=6, fill='x')

        self.submit_btn = tk.Button(self.btn_frame, text='Submit', command=self.evaluate_answer, width=12)
        self.submit_btn.pack(side='left')

        self.next_btn = tk.Button(self.btn_frame, text='Next question', command=self.next_question, width=14)
        self.next_btn.pack(side='left', padx=8)

        self.show_btn = tk.Button(self.btn_frame, text='Show answer (instructor)', command=self.show_answer, width=18)
        self.show_btn.pack(side='left')

        self.export_btn = tk.Button(self.btn_frame, text='Export log', command=self.export_log, width=12)
        self.export_btn.pack(side='right')

        # Rezultat
        self.result_label = tk.Label(master, text='', font=('Arial', 12, 'bold'))
        self.result_label.pack(padx=10, pady=(6, 10), anchor='w')

        # Stare (puțin schimbată)
        self.current_scenario = None  # Aici stocăm tot dicționarul scenariului
        self.log = load_log()

        # Inițializare
        self.next_question()

    def next_question(self):
        """
        *** AICI ESTE MODIFICAREA PRINCIPALĂ ***
        Selectează un scenariu și construiește întrebarea.
        """
        self.answer_entry.delete('1.0', tk.END)
        self.result_label.config(text='')

        # 1. Alege aleatoriu un scenariu din Baza de Cunoștințe
        self.current_scenario = random.choice(KB_TYPE_1_SCENARIOS)

        # 2. Construiește textul întrebării din bucățile scenariului
        q_text = (
            f"Pentru problema '{self.current_scenario['problem']}', "
            f"pe o {self.current_scenario['instance']}, "
            f"care este cea mai potrivită strategie {self.current_scenario['goal']}"
        )

        # 3. Actualizează interfața grafică
        self.question_text.config(text=q_text)

    def evaluate_answer(self):
        """
        *** MICĂ MODIFICARE AICI ***
        Extrage listele de răspunsuri din self.current_scenario
        """
        user_ans = self.answer_entry.get('1.0', tk.END).strip()
        if not user_ans:
            messagebox.showwarning('Atenție', 'Te rog introdu un răspuns înainte de submit.')
            return

        # Extragem listele din scenariul curent
        correct_answers = self.current_scenario.get('answers', [])
        wrong_kws = self.current_scenario.get('wrong_keywords', [])

        # Apelul funcției de evaluare rămâne identic!
        score = evaluate_strategy_answer(user_ans, correct_answers, wrong_kws)

        self.result_label.config(text=f'Scor evaluare: {score}%')

        # Logarea este acum mai completă
        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'scenario_id': self.current_scenario['id'],
            'question': self.question_text.cget("text"),  # Salvăm textul complet
            'user_answer': user_ans,
            'correct_answers': correct_answers,
            'wrong_keywords': wrong_kws,
            'score': score
        }
        self.log.append(entry)
        save_log(self.log)

        messagebox.showinfo('Rezultat', f'Răspuns evaluat: {score}%')

    def show_answer(self):
        """
Afișează răspunsurile corecte din scenariul curent.
"""
        if not self.current_scenario:
            return
        ca = '\n'.join(self.current_scenario.get('answers', ['N/A']))
        messagebox.showinfo('Răspuns corect (intern)', 'Răspunsuri posibile:\n' + ca)

    # Funcția `export_log` rămâne la fel ca înainte

    # ... (restul codului tău, `if __name__ == '__main__':` etc.) ...
    def export_log(self):
        if not self.log:
            messagebox.showinfo('Export log', 'Nu există interacțiuni de exportat.')
            return
        filename = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files', '*.json')],
                                                title='Salveaza log ca...')
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.log, f, ensure_ascii=False, indent=2)
            messagebox.showinfo('Export log', f'Log salvat: {filename}')


if __name__ == '__main__':
    root = tk.Tk()
    app = SmarTestApp(root)
    root.mainloop()
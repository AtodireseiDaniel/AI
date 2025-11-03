import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import random
import json
import difflib
import string
from datetime import datetime

# --- MODEL 2: BAZA DE CUNOȘTINȚE (DOAR N-QUEENS) ---
# --- MODEL 3: BAZA DE CUNOȘTINȚE (DOAR CELE 4 PROBLEME) ---
# Această listă se concentrează exclusiv pe cele 4 probleme din cerința minimă
# și leagă de conceptele din curs (Backtracking, MRV, Hillclimbing, etc.)

KB_TYPE_1_NQUEENS_ONLY = [

    # --- 1. SCENARII PENTRU GRAPH COLORING ---
    {
        'id': 'graph-color-small-optimal',
        'problem': 'Graph Coloring (Colorarea Grafurilor)',
        'instance': 'o instanță mică (ex: harta a 10 țări)',
        'goal': 'pentru a garanta găsirea numărului *minim* de culori (soluția optimă)? [Ref: Curs CSP]',
        'answers': [
            'backtracking',
            'constraint satisfaction',
            'csp',
            'algoritm complet'
        ],
        'wrong_keywords': [
            'greedy', 'hill climbing', 'euristic', 'min-conflicts'
        ]
    },
    {
        'id': 'graph-color-large-heuristic',
        'problem': 'Graph Coloring (Colorarea Grafurilor)',
        'instance': 'o instanță foarte mare (ex: orarul unei universități)',
        'goal': 'pentru a găsi o soluție "suficient de bună" (nu neapărat optimă) cât mai rapid? [Ref: Curs S4]',
        'answers': [
            'greedy',
            'euristic',
            'algoritm greedy'
        ],
        'wrong_keywords': [
            'backtracking', 'constraint satisfaction', 'csp'
        ]
    },
    {
        'id': 'graph-color-mrv-heuristic',
        'problem': 'Graph Coloring (Colorarea Grafurilor)',
        'instance': 'în timpul rulării Backtracking, pentru a alege următoarea *regiune* (variabilă) de colorat',
        'goal': 'ce euristică "fail-first" (alege regiunea cu cele mai puține culori legale rămase) ar trebui folosită? [Ref: Curs S4, pg. 25]',
        'answers': [
            'mrv (minimum-remaining-values)',
            'minimum remaining values',
            'variabila cea mai constrânsă'
        ],
        'wrong_keywords': [
            'lcv (least-constraining-value)', 'forward checking', 'ac-3'
        ]
    },

    # --- 2. SCENARII PENTRU N-QUEENS ---
    {
        'id': 'n-queens-small-optimal',
        'problem': 'N-Queens',
        'instance': 'o instanță mică (ex: N=8)',
        'goal': 'pentru a găsi *toate* soluțiile posibile? [Ref: Curs S2, S4]',
        'answers': [
            'backtracking',
            'căutare exhaustivă',
            'algoritm complet'
        ],
        'wrong_keywords': [
            'hill climbing', 'greedy', 'heuristic', 'min-conflicts'
        ]
    },
    {
        'id': 'n-queens-large-heuristic',
        'problem': 'N-Queens',
        'instance': 'o instanță foarte mare (ex: N=1,000,000)',
        'goal': 'pentru a găsi *o singură* soluție cât mai rapid? [Ref: Curs S4, pg. 54-57]',
        'answers': [
            'min-conflicts',
            'hill climbing',
            'local search (căutare locală)',
            'euristic'
        ],
        'wrong_keywords': [
            'backtracking', 'algoritm complet', 'bfs', 'a*'
        ]
    },
    {
        'id': 'n-queens-local-optimum-problem',
        'problem': 'N-Queens',
        'instance': 'când se folosește o strategie de Căutare Locală (Min-Conflicts / Hillclimbing)',
        'goal': 'care este principalul risc care poate bloca algoritmul înainte de a găsi soluția globală? [Ref: Curs S3, pg. 12]',
        'answers': [
            'blocarea în maxime locale',
            'local optimum'
        ],
        'wrong_keywords': [
            'memorie (costly)', 'bucle infinite (loops)', 'a*'
        ]
    },

    # --- 3. SCENARII PENTRU HANOI TOWERS ---
    {
        'id': 'hanoi-representation',
        'problem': 'Generalized Hanoi Towers (Turnurile Hanoi)',
        'instance': 'la începutul modelării problemei (cu $m$ piese și $n$ tije)',
        'goal': 'care este (conform cursului) cel mai important și dificil pas inițial? [Ref: Curs S2, pg. 14]',
        'answers': [
            'alegerea reprezentării stării',
            'reprezentarea stării',
            'choosing a representation for a state'
        ],
        'wrong_keywords': [
            'backtracking', 'bfs', 'strategia de căutare', 'hill climbing'
        ]
    },
    {
        'id': 'hanoi-strategy-type',
        'problem': 'Generalized Hanoi Towers (Turnurile Hanoi)',
        'instance': 'pentru a găsi soluția optimă (numărul minim de mutări)',
        'goal': 'ce strategie clasică, bazată pe "Divide and Conquer", este folosită pentru a rezolva problema?',
        'answers': [
            'recursion',
            'recursive solution',
            'algoritm recursiv',
            'divide and conquer'
        ],
        'wrong_keywords': [
            'backtracking', 'hill climbing', 'greedy', 'min-conflicts'
        ]
    },

    # --- 4. SCENARII PENTRU KNIGHT'S TOUR ---
    {
        'id': 'knights-tour-csp-base',
        'problem': "Knight's Tour (Turul Calului)",
        'instance': 'o instanță unde trebuie găsit un drum complet (o soluție)',
        'goal': 'ce strategie de bază, neinformată, care nu necesită memorarea stărilor vizitate, este folosită pentru a căuta o soluție? [Ref: Curs S2, pg. 25]',
        'answers': [
            'backtracking'
        ],
        'wrong_keywords': [
            'bfs', 'dfs', 'hill climbing', 'greedy', 'minimax'
        ]
    },
    {
        'id': 'knights-tour-heuristic',
        'problem': "Knight's Tour (Turul Calului)",
        'instance': 'pentru a găsi o soluție *eficient* (a ghida algoritmul Backtracking)',
        'goal': 'ce euristică faimoasă (o formă de MRV) este folosită pentru a alege următoarea mutare?',
        'answers': [
            "warnsdorff's heuristic",
            'euristica warnsdorff',
            'warnsdorff'
        ],
        'wrong_keywords': [
            'lcv', 'min-conflicts', 'a*', 'greedy'
        ]
    }
]

# --- LISTA GLOBALĂ A CUVINTELOR CHEIE DE ALGORITM ---
GLOBAL_ALGORITHM_KEYWORDS = {
    'bfs', 'breadth', 'first', 'search', 'uniform', 'cost', 'dfs', 'depth',
    'backtracking', 'ids', 'iterative', 'deepening', 'bidirectional', 'random',
    'lățime', 'adâncime', 'iterativă', 'greedy', 'best-first', 'hillclimbing', 'hill',
    'climbing', 'simulated', 'annealing', 'recoacere', 'simulată', 'beam', 'a*',
    'star', 'ida*', 'heuristic', 'euristic', 'admisibilă', 'mrv', 'minimum',
    'remaining', 'values', 'lcv', 'least', 'constraining', 'value', 'forward',
    'checking', 'ac-3', 'arc', 'consistency', 'min-conflicts', 'conflicts',
    'backjumping', 'minimax', 'alpha', 'beta', 'pruning', 'nash'
}

LOG_FILE = 'log_interactions_nqueens_model.json'


# --- Funcția de Normalizare a Textului ---
def normalize_text(s):
    s = s.lower()
    s = s.translate(str.maketrans('', '', string.punctuation))
    return ' '.join(s.strip().split())


# --- Funcția de Evaluare "Pseudo-Semantică" (Non-AI) ---
# (Versiunea strictă, cu "verificarea contaminării")
def evaluate_strategy_answer(user_answer, correct_answers_list, wrong_keywords_list, similarity_threshold=0.6):
    ua_norm = normalize_text(user_answer)
    if not ua_norm:
        return 0

    user_words = set(ua_norm.split())

    # 1. Extragem seturile de cuvinte cheie
    correct_keywords = set()
    for ans in correct_answers_list:
        for word in normalize_text(ans).split():
            correct_keywords.add(word)

    wrong_keywords = set()
    for kw_list in wrong_keywords_list:
        for word in normalize_text(kw_list).split():
            wrong_keywords.add(word)

    # 2. Verificarea Listei Negre Explicite
    if any(word in wrong_keywords for word in user_words):
        return 0

        # 3. Verificarea Listei Albe
    found_correct = False
    if any(word in correct_keywords for word in user_words):
        found_correct = True

    # 4. Verificarea Contaminării (Globală)
    contamination_set = GLOBAL_ALGORITHM_KEYWORDS - correct_keywords
    found_contamination = False
    if any(word in contamination_set for word in user_words):
        found_contamination = True

    # 5. Logica de Decizie
    if found_correct and not found_contamination:
        return 100

    if found_correct and found_contamination:
        # Ex: Răspuns: "backtracking și min-conflicts" (amestecă algoritmi)
        return 0

    if not found_correct and found_contamination:
        # Ex: Răspuns: "greedy" (un alt algoritm, complet greșit)
        return 0

        # 6. Fallback (Typos)
    if not found_correct and not found_contamination:
        best_ratio = 0.0
        for ans in correct_answers_list:
            ans_norm = normalize_text(ans)
            ratio = difflib.SequenceMatcher(None, ua_norm, ans_norm).ratio()
            if ratio > best_ratio:
                best_ratio = ratio

        if best_ratio >= similarity_threshold:
            return int(best_ratio * 100)
        else:
            return 0

    return 0


# ----- Functii pentru log -----
def load_log():
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_log(log):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


# ----- Aplicatie GUI -----
class SmarTestApp:
    def __init__(self, master):
        self.master = master
        master.title('SmarTest - Model 2 (DOAR N-Queens)')
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

        # Stare
        self.current_scenario = None
        self.log = load_log()
        self.next_question()

    def next_question(self):
        self.answer_entry.delete('1.0', tk.END)
        self.result_label.config(text='')

        # --- AICI ESTE SINGURA SCHIMBARE ---
        # Alege o întrebare aleatorie DOAR din lista N-Queens
        self.current_scenario = random.choice(KB_TYPE_1_NQUEENS_ONLY)
        # --- SFÂRȘIT SCHIMBARE ---

        q_text = (
            f"Pentru problema '{self.current_scenario['problem']}', "
            f"pe o {self.current_scenario['instance']}, "
            f"care este cea mai potrivită strategie {self.current_scenario['goal']}"
        )
        self.question_text.config(text=q_text)

    def evaluate_answer(self):
        user_ans = self.answer_entry.get('1.0', tk.END).strip()
        if not user_ans:
            messagebox.showwarning('Atenție', 'Te rog introdu un răspuns înainte de submit.')
            return

        correct_answers = self.current_scenario.get('answers', [])
        wrong_kws = self.current_scenario.get('wrong_keywords', [])

        score = evaluate_strategy_answer(user_ans, correct_answers, wrong_kws)

        self.result_label.config(text=f'Scor evaluare: {score}%')

        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'scenario_id': self.current_scenario['id'],
            'question': self.question_text.cget("text"),
            'user_answer': user_ans,
            'correct_answers': correct_answers,
            'wrong_keywords': wrong_kws,
            'score': score
        }
        self.log.append(entry)
        save_log(self.log)
        messagebox.showinfo('Rezultat', f'Răspuns evaluat: {score}%')

    def show_answer(self):
        if not self.current_scenario:
            return
        ca = '\n'.join(self.current_scenario.get('answers', ['N/A']))
        messagebox.showinfo('Răspuns corect (intern)', 'Răspunsuri posibile:\n' + ca)

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
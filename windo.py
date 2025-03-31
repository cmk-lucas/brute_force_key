import tkinter as tk
from tkinter import filedialog, messagebox
import itertools
import string
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor

# Dictionnaire intégré (peut être remplacé par un fichier externe)
DICTIONARY = [
    "123456", "password", "123456789", "qwerty", "abc123", "admin",
    "letmein", "welcome", "monkey", "football", "iloveyou", "passw0rd"
]

def hash_password(password, algorithm="sha256"):
    """Retourne le hash du mot de passe selon l'algorithme choisi."""
    return hashlib.new(algorithm, password.encode()).hexdigest()

def dictionary_attack(password, hash_mode=False, algorithm="sha256"):
    """Teste d'abord les mots du dictionnaire avant le brute-force."""
    for attempt in DICTIONARY:
        test_value = hash_password(attempt, algorithm) if hash_mode else attempt
        print(f"[*] Test (dictionnaire) : {attempt}")
        if test_value == password:
            return attempt
    return None

def load_wordlist(file_path):
    """Charge un fichier de mots de passe."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print("[⚠] Fichier introuvable.")
        return []

def mutate_password(password):
    """Génère des variantes du mot de passe (admin → Admin123!)."""
    return [
        password,
        password.capitalize(),
        password + "123",
        password + "!",
        password.replace("a", "@").replace("o", "0").replace("e", "3")
    ]

def brute_force(password, min_length=1, max_length=4, show_attempts=False, hash_mode=False, algorithm="sha256"):
    """
    Tente de deviner un mot de passe via dictionnaire puis brute-force.
    """
    start_time = time.time()
    
    # 1️⃣ Attaque dictionnaire (y compris avec hash)
    found = dictionary_attack(password, hash_mode, algorithm)
    if found:
        return generate_report(found, len(DICTIONARY), time.time() - start_time, "Dictionnaire")

    # 2️⃣ Mutation des mots de passe du dictionnaire
    for word in DICTIONARY:
        for variation in mutate_password(word):
            print(f"[*] Test (mutation) : {variation}")
            if variation == password:
                return generate_report(variation, len(DICTIONARY), time.time() - start_time, "Mutation")

    # 3️⃣ Brute-force total
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    attempts = len(DICTIONARY)

    def test_guess(guess):
        return hash_password(guess, algorithm) if hash_mode else guess

    with ThreadPoolExecutor(max_workers=4) as executor:
        for length in range(min_length, max_length + 1):
            for guess_tuple in itertools.product(characters, repeat=length):
                guess = ''.join(guess_tuple)
                attempts += 1
                if show_attempts:
                    print(f"[*] Tentative {attempts}: {guess}")

                if test_guess(guess) == password:
                    return generate_report(guess, attempts, time.time() - start_time, "Brute-force")

    return None

def generate_report(password_found, attempts, time_taken, method):
    """Génère un rapport des tests de mot de passe."""
    report = f"""
    === Rapport de test ===
    Mot de passe trouvé : {password_found}
    Nombre d'essais : {attempts}
    Temps écoulé : {time_taken:.2f} secondes
    Méthode utilisée : {method}
    """
    print(report)
    with open("rapport.txt", "w") as f:
        f.write(report)
    return {
        "mot_de_passe": password_found,
        "essais": attempts,
        "temps": round(time_taken, 2),
        "méthode": method
    }

if __name__ == "__main__":
    mot_de_passe = input("Entrez le mot de passe à deviner : ").strip()
    hash_mode = input("Le mot de passe est-il en hash ? (o/n) : ").lower() == 'o'
    algo = "sha256"

    if hash_mode:
        algo = input("Entrez l'algorithme de hash (md5, sha256, sha1...) : ").strip()
    
    while True:
        try:
            min_length = int(input("Longueur minimale du mot de passe : "))
            max_length = int(input("Longueur maximale du mot de passe : "))
            if min_length > max_length or min_length < 1:
                print("Longueur invalide.")
                continue
            break
        except ValueError:
            print("Veuillez entrer des nombres valides.")

    show_attempts = input("Afficher les tentatives ? (o/n) : ").lower() == 'o'

    # Test avec une wordlist externe
    use_wordlist = input("Utiliser un fichier de wordlist ? (o/n) : ").lower() == 'o'
    if use_wordlist:
        file_path = input("Chemin du fichier de wordlist : ").strip()
        wordlist = load_wordlist(file_path)
        for word in wordlist:
            if word == mot_de_passe:
                generate_report(word, len(wordlist), 0, "Wordlist externe")
                exit()

    resultat = brute_force(mot_de_passe, min_length, max_length, show_attempts, hash_mode, algo)

    if not resultat:
        print("\n[✖] Mot de passe non trouvé.")

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("BruteForce Tool")
root.geometry("400x300")

tk.Label(root, text="Mot de passe :").pack()
entry_password = tk.Entry(root)
entry_password.pack()

tk.Label(root, text="Longueur min :").pack()
entry_min_len = tk.Entry(root)
entry_min_len.insert(0, "1")
entry_min_len.pack()

tk.Label(root, text="Longueur max :").pack()
entry_max_len = tk.Entry(root)
entry_max_len.insert(0, "4")
entry_max_len.pack()

var_hash = tk.BooleanVar()
tk.Checkbutton(root, text="Le mot de passe est en hash", variable=var_hash).pack()

tk.Button(root, text="Lancer l'attaque", command=run_attack).pack()
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
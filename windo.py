import itertools
import string
import time

def brute_force(password, min_length=1, max_length=4, show_attempts=False):
    """
    Tente de deviner un mot de passe en générant toutes les combinaisons possibles.
    
    Args:
        password (str): Le mot de passe à deviner.
        min_length (int): Longueur minimale du mot de passe.
        max_length (int): Longueur maximale du mot de passe.
        show_attempts (bool): Affiche chaque tentative si True.

    Returns:
        dict ou None: Détails si réussi, sinon None.
    """
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    attempts = 0
    start_time = time.time()

    for length in range(min_length, max_length + 1):
        for guess in itertools.product(characters, repeat=length):
            guess = ''.join(guess)
            attempts += 1
            if show_attempts:
                print(f"[*] Tentative {attempts}: {guess}")

            if guess == password:
                duration = time.time() - start_time
                return {
                    'mot_de_passe': guess,
                    'essais': attempts,
                    'temps': round(duration, 2)
                }

    return None

if __name__ == "__main__":
    # Demande le mot de passe et les paramètres à l'utilisateur
    mot_de_passe = input("Entrez le mot de passe à deviner : ").strip()
    
    while True:
        try:
            min_length = int(input("Longueur minimale du mot de passe : "))
            max_length = int(input("Longueur maximale du mot de passe : "))
            if min_length > max_length or min_length < 1:
                print("La longueur minimale doit être inférieure ou égale à la longueur maximale et positive.")
                continue
            break
        except ValueError:
            print("Veuillez entrer des nombres valides.")

    show_attempts = input("Afficher les tentatives ? (o/n) : ").lower() == 'o'

    resultat = brute_force(mot_de_passe, min_length, max_length, show_attempts)

    if resultat:
        print(f"\n[✔] Mot de passe trouvé: {resultat['mot_de_passe']}")
        print(f"[🔢] Nombre d'essais: {resultat['essais']}")
        print(f"[⏳] Temps pris: {resultat['temps']} secondes")
    else:
        print("\n[✖] Mot de passe non trouvé.")

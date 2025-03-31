import itertools  
import string  
import time  

def brute_force(password, min_length=1, max_length=4):  
    # Définir les caractères possibles : lettres minuscules, majuscules et chiffres  
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits  
    
    # Garder une trace du nombre d'essais  
    attempts = 0  
    
    # Commencer le chronomètre  
    start_time = time.time()  
    
    # Essayer des mots de passe de différentes longueurs  
    for length in range(min_length, max_length + 1):  
        for guess in itertools.product(characters, repeat=length):  
            guess = ''.join(guess)  # Convertir le tuple en chaîne de caractères  
            attempts += 1  
            if guess == password:  
                end_time = time.time()  
                duration = end_time - start_time  
                return {  
                    'mot_de_passe': guess,  
                    'essais': attempts,  
                    'temps': duration  
                }  
    
    return None  # Aucun mot de passe trouvé  

# Exemple d'utilisation  
if __name__ == "__main__":  
    mot_de_passe = input("Entrez le mot de passe à deviner : ")  # Demande le mot de passe à deviner  
    min_length = int(input("Entrez la longueur minimale du mot de passe : "))  
    max_length = int(input("Entrez la longueur maximale du mot de passe : "))  
    
    resultat = brute_force(mot_de_passe, min_length, max_length)  
    
    if resultat:  
        print(f'Mot de passe trouvé: {resultat["mot_de_passe"]}')  
        print(f'Nombre d\'essais: {resultat["essais"]}')  
        print(f'Temps pris: {resultat["temps"]:.2f} secondes')  
    else:  
        print("Mot de passe non trouvé.")  
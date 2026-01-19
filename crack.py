import hashlib
import sys

def crack():
    if len(sys.argv) != 3:
        print("Ús: python3 crack.py diccionari.txt HASH_OBJECTIU")
        return

    diccionari_fitxer = sys.argv[1]
    hash_objectiu = sys.argv[2]
   
    # El salt a Linux sol ser la part entre el 2n i 3r símbol de '$'
    # Exemple: $6$salt$hash... -> salt és la part 3
    try:
        parts = hash_objectiu.split('$')
        id_algoritme = parts[1]
        salt = parts[2]
    except IndexError:
        print("Error: El format del hash no és correcte.")
        return

    try:
        with open(diccionari_fitxer, 'r', encoding='latin-1') as f:
            for linea in f:
                paraula = linea.strip()
                # mkpasswd -m sha-512 usa l'algoritme 6 de crypt
                # Nota: Python requereix la llibreria crypt (nativa en Linux)
                import crypt
                hash_calculat = crypt.crypt(paraula, f"${id_algoritme}${salt}$")
               
                if hash_calculat == hash_objectiu:
                    print("-" * 40)
                    print(f"CONTRASENYA TROBADA: {paraula}")
                    print("-" * 40)
                    return
    except FileNotFoundError:
        print("Error: No s'ha trobat el fitxer de diccionari.")

    print("No s'ha trobat la contrasenya al diccionari.")

if __name__ == "__main__":
    crack()

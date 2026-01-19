#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Ús: $0 diccionari.txt HASH_OBJECTIU"
    exit 1
fi

DICCIONARI=$1
HASH_OBJECTIU=$2
SALT=$(echo "$HASH_OBJECTIU" | cut -d'$' -f3)

while read -r paraula; do
    # Neteja caràcters invisibles i salts de línia
    paraula=$(echo -n "$paraula" | tr -d '\r\n')
   
    # Genera el hash usant el mateix SALT que la contrasenya objectiu
    hash_calculat=$(mkpasswd -m sha-512 -S "$SALT" "$paraula")
   
    # Compara el hash generat amb l'objectiu
    if [ "$hash_calculat" = "$HASH_OBJECTIU" ]; then
        echo "--------------------------------------------------"
        echo "La contrasenya ha estat compromesa: $paraula"
        echo "--------------------------------------------------"
        exit 0
    fi
done < "$DICCIONARI"

echo "No s'ha trobat la contrasenya al fitxer de diccionari."

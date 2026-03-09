# Signature et Chiffrement de Fichier avec ECC (Style Blockchain)

Ce projet implémente un système de sécurisation de fichiers basé sur la cryptographie sur les courbes elliptiques (ECC), simulant le processus de sécurisation des données dans une **Blockchain**. 
Le système assure l'**authenticité** via la signature numérique (ECDSA) et la **confidentialité** via le chiffrement symétrique (AES) avec un échange de clés sécurisé (ECDH).
##  Prérequis

* **Langage :** Python
* **Bibliothèque :** `cryptography`
* **Installation :** `pip install cryptography`

## Structure du Projet

Le projet se compose de trois scripts principaux :
1. **`generate_key.py`** : Génère les paires de clés privées et publiques nécessaires pour la signature et l'échange de clés.
2. **`alice.py`** (Expéditeur) : Signe le fichier, établit un secret partagé et chiffre le contenu.
3. **`bob.py`** (Destinataire) : Reconstitue la clé, déchiffre le fichier et vérifie la signature.

---
## Mode Opératoire
Suivez ces étapes dans l'ordre pour valider le fonctionnement de la solution :
- ### 1. Préparation des données
Assurez-vous d'avoir un fichier texte nommé `fichier.txt` à la racine du projet contenant votre message (ex: "bonjour").
- ### 2. Génération des clés
Exécutez le script pour créer l'identité cryptographique des deux parties :
```bash
python generate_key.py
```
- ### 3. Phase d'expédition (côté Alice)
```bash
python alice.py
```
- ### 4. Phase de reception (côté bob)
```bash
python bob.py
```

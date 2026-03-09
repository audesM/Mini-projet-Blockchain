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

## Résultat 
Génération des clés de alice et bob 
### 1. Execution de generate_key.py
- ### Clés d'alice
<img width="282" height="110" alt="image" src="https://github.com/user-attachments/assets/a74d3021-d0fe-45ca-9af1-c63384d79726" />

- ### clés de bob
<img width="324" height="106" alt="image" src="https://github.com/user-attachments/assets/495fca91-ffd9-4c75-a84d-63bb6fea253a" />

### 2. Méssage crypté
<img width="349" height="96" alt="image" src="https://github.com/user-attachments/assets/d4f17c2e-b2ac-4e7b-81e8-c4cfa0ac6221" />
<img width="1215" height="157" alt="image" src="https://github.com/user-attachments/assets/6941fc63-a68d-4e6c-86ad-fd4ce7337b95" />





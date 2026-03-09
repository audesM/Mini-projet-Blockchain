# bob.py
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def load_private_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def sha256_data(data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()

def main(packet_dir):
    # Charger clés Bob
    bob_ecdh_priv = load_private_key("bob_ecdh_private.pem")

    # Charger clés publiques Alice
    alice_sign_pub = load_public_key(f"{packet_dir}/alice_sign_private.pem")
    alice_ecdh_pub = load_public_key(f"{packet_dir}/alice_ecdh_public.pem")

    # Charger fichiers
    with open(f"{packet_dir}/encrypted_file.bin", "rb") as f:
        data = f.read()
    iv, ciphertext = data[:16], data[16:]

    with open(f"{packet_dir}/signature.sig", "rb") as f:
        signature = f.read()

    with open(f"{packet_dir}/metadata.json", "r") as f:
        metadata = json.load(f)

    # Reconstituer clé AES via ECDH
    shared_secret = bob_ecdh_priv.exchange(ec.ECDH(), alice_ecdh_pub)
    derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"AES").derive(shared_secret)

    # Déchiffrement
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Vérification hash
    recalculated_hash = sha256_data(plaintext)

    try:
        alice_sign_pub.verify(signature, recalculated_hash, ec.ECDSA(hashes.SHA256()))
        if recalculated_hash.hex() == metadata["hash"]:
            print(" Signature valide - Fichier authentique")
        else:
            print(" Fichier altéré")
    except Exception:
        print("Signature invalide")

    # Sauvegarde fichier déchiffré
    with open("received_file.txt", "wb") as f:
        f.write(plaintext)

if __name__ == "__main__":
    main("packet")

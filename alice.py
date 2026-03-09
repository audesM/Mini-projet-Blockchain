import os, json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def load_private_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def sha256_file(filename):
    digest = hashes.Hash(hashes.SHA256())
    with open(filename, "rb") as f:
        digest.update(f.read())
    return digest.finalize()

def encrypt_file(filename, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    with open(filename, "rb") as f:
        plaintext = f.read()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv, ciphertext

def main(file_to_send):
    os.makedirs("packet", exist_ok=True)

    # Charger clés Alice
    alice_sign_priv = load_private_key("alice_sign_private.pem")
    alice_ecdh_priv = load_private_key("alice_ecdh_private.pem")

    # Charger clé publique Bob
    bob_ecdh_pub = load_public_key("bob_ecdh_public.pem")

    # Hash du fichier
    file_hash = sha256_file(file_to_send)

    # Signature
    signature = alice_sign_priv.sign(file_hash, ec.ECDSA(hashes.SHA256()))

    # Secret partagé via ECDH
    shared_secret = alice_ecdh_priv.exchange(ec.ECDH(), bob_ecdh_pub)
    derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"AES").derive(shared_secret)

    # Chiffrement AES
    iv, ciphertext = encrypt_file(file_to_send, derived_key)

    # Sauvegarde packet
    with open("packet/encrypted_file.bin", "wb") as f:
        f.write(iv + ciphertext)
    with open("packet/signature.sig", "wb") as f:
        f.write(signature)
    with open("packet/alice_pub_sign.pem", "wb") as f:
        f.write(alice_sign_priv.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    with open("packet/alice_pub_ecdh.pem", "wb") as f:
        f.write(alice_ecdh_priv.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    metadata = {
        "filename": file_to_send,
        "size": os.path.getsize(file_to_send),
        "hash": file_hash.hex()
    }
    with open("packet/metadata.json", "w") as f:
        json.dump(metadata, f)

    print("Packet généré avec succès.")

if __name__ == "__main__":
    main("fichier.txt")

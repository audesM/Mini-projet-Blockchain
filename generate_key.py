from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_key_pair(filename_prefix):
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    # Sauvegarde clé privée
    with open(f"{filename_prefix}_private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Sauvegarde clé publique
    with open(f"{filename_prefix}_public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"Clés générées pour {filename_prefix}")

if __name__ == "__main__":
    generate_key_pair("alice_sign")
    generate_key_pair("alice_ecdh")
    generate_key_pair("bob_sign")
    generate_key_pair("bob_ecdh")

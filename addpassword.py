import hashlib 
import secrets

passw = input("input new password: ")
passwcheck = input("verify password: ")

if passw == passwcheck:
    myhash = hashlib.sha256()
    myhash.update(passw.encode("utf-8"))
    print(myhash.digest())
    with open("secrets.py", "w") as secretsfile:
        secretsfile.write(f"cookie = '{secrets.cookie}'\n")
        secretsfile.write(f"passwords = [\n")
        for i in secrets.passwords:
            secretsfile.write(f"\t{i},\n")
        secretsfile.write(f"\t{myhash.digest()},\n")
        secretsfile.write(f"]")
else:
    print("passwords do not match")





import hashlib 
import mysecrets
import sys
import random 
import string

def main():
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        if flag == "-a":
            if len(sys.argv) > 2:
                addpass(sys.argv[2])
            else:
                addpass()
        elif flag == "-c":
            reset_cookie()
        elif flag == "-r":
            if len(sys.argv) > 2:
                remove_pass(sys.argv[2])
            else:
                remove_pass()
        else:
            help()
    else: 
        help()

def addpass(passw = None):
    if not passw:
        passw = input("input new password: ")
        passwcheck = input("verify password: ")
        if passw != passwcheck:
            print("passwords do not match")
            return
    myhash = hashlib.sha256()
    myhash.update(passw.encode("utf-8"))
    print(myhash.digest())
    with open("mysecrets.py", "w") as secretsfile:
        secretsfile.write(f"cookie = '{mysecrets.cookie}'\n")
        secretsfile.write(f"passwords = [\n")
        for i in mysecrets.passwords:
            secretsfile.write(f"\t{i},\n")
        secretsfile.write(f"\t{myhash.digest()},\n")
        secretsfile.write(f"]")


def remove_pass(passw = None):
    if not passw:
        passw = input("enter password to remove: ")
    passhash = hashlib.sha256(passw.encode('utf-8')).digest()
    try:
        mysecrets.passwords.remove(passhash)
    except ValueError:
        print("password is not in list")

    with open("mysecrets.py", "w") as secretsfile:
            secretsfile.write(f"cookie = '{mysecrets.cookie}'\n")
            secretsfile.write(f"passwords = [\n")
            for i in mysecrets.passwords:
                secretsfile.write(f"\t{i},\n")
            secretsfile.write(f"]")



def reset_cookie():
    new_cookie = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(50)])
    with open("mysecrets.py", "w") as secretsfile:
            secretsfile.write(f"cookie = '{new_cookie}'\n")
            secretsfile.write(f"passwords = [\n")
            for i in mysecrets.passwords:
                secretsfile.write(f"\t{i},\n")
            secretsfile.write(f"]")
    print(new_cookie)

def help():
    print("-a\tadd password")
    print("-r\tremove password")
    print("-c\treset cookie")


if __name__ == "__main__":
    main()

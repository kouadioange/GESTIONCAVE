from ast import If
import string
import random
def reference():
    chiffre = string.digits
    lettre = string.ascii_uppercase
    l=7
    char = chiffre+lettre
    reference = "".join(random.choices(char,k=l))

    return "ref-" + reference

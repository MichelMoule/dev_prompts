print("Bienvenue dans le programme de calcul de somme!"  # <-- Il manque une parenthèse fermante

nums = []
for i in range(3):
  val = input("Entrez un nombre : ")  # <-- Les valeurs récupérées sont des chaînes de caractères, pas des entiers
  nums.append(val)

sum_of_nums = sum(nums)  # <-- sum sur des chaînes de caractères ne fonctionnera pas
print("La somme des nombres est: " sum_of_nums)  # <-- Manque un signe de concaténation ou virgule

if sum_of_nums > 10:
print("La somme est plus grande que 10 !")  # <-- Problème d'indentation
 else:
  print("La somme est inférieure ou égale à 10.")

average = sum_of_nums / len(num)  # <-- 'num' n'existe pas, la liste s'appelle 'nums'
print("La moyenne est :", average)

# ALL QUESTIONS HAVE BEEN COMPLETED USING PYTHON 3.9.5!
#
# Print a random integer in the range 20 to 25.
#
# print(__import__("random").randint(20, 25))
#
# Write a program that stores your age in a variable. Double the value and print it.
#
# print(age := (age := 7) * 2)
#
# Create an empty list. Using the random module, add eight random integers (from 1 to 100) to the list.
# Iterate over the list and print only the odd numbers in the list.
#
# [print(i) for i in [] + [__import__("random").randint(1, 100) for _ in range(8)] if i % 2 == 1]
#
# Ask the user to enter a word. Using a while loop, print the word in reverse order. For example:
# Enter a word: computer
# Output: retupmoc
#
# while (index := (index - 1) if "index" in globals() else -1) >= -len(word := input("Enter a word: ") if "word" not in globals() else word): print(end=word[index])
#
# Ask the user to enter a few numbers separated by spaces. When the user presses the enter/return key on the keyboard,
# print the average of those numbers along with the count of numbers entered by the user. For example:
# Enter a few numbers separated by spaces: 2 5 6 7 10
# Output: 6.0 5
# Tip: Average is 6.0 and there are 5 numbers entered by the user
#
# print(sum(numbers := list(map(int, input("Enter some numbers: ").split()))) / len(numbers), len(numbers))
#
# Write a function that takes an integer as an argument and returns a random string with as many letters as the integer.
# Call the function and print the returned string. Example: random_string(3) returns "aed".
# Tip: You can use the chr function or the string module
#
# print((lambda x: "".join(__import__("random").choice(list(map(chr, range(97, 123)))) for _ in range(x)))(3))
#
# Ask the user to input an integer. Generate a dictionary with keys from 1 to the number (included).
# Set their values to be the square root of the corresponding key. Print the dictionary. Example:
# Enter a number: 3
# Output:
# {1: 1, 2: 1.41.., 3: 1.73..}
# Tip: x ** 0.5 gives the square root of x.
#
# print({i: i**0.5 for i in range(1, int(input("Type an integer: "))+1)})
#
# Write a function that takes three integer arguments and returns the smallest integer without using the min function.
# Call the function and print the returned result. For example: min_finder(3, 6, 1) returns 1.
#
# print((lambda a, b, c: sorted([a, b, c])[0])(3, 6, 1))
#
# Create a list to store the names of five fruits. Use the random module to shuffle the letters of each fruit such that
# the list contains the shuffled fruit names. Print the list.
# Example:
# fruits = ["Apple", "Banana", "Pear", "Pineapple", "Guava"]
# Output:
# ["eAplp", "aaBnan", "reaP", "neeiaPplp", "vuaGa"]
#
# print(["".join(__import__("random").sample(fruit, len(fruit))) for fruit in ["Apple", "Banana", "Pear", "Pineapple", "Guava"]])

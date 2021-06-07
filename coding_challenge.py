# Write a program that creates three variables that store an integer, a floating point number and a string respectively.
# Print all the three variables in the same line.

# print(a := 1, b := 2.0, c := "3")

# Write a program that runs a while loop to print numbers from 2 to 23.

# x = 1
# while (x := x + 1) < 24: print(x)

# Write a program that asks the user for their first name. Print the name followed by the number of characters in it.
# There should not be any space between the name and the number of characters. For example,
# Please enter your first name: Silvers
# Output: Silvers7

# print(first := input("What is your first name? "), str(len(first)), sep="")

# Create a list of six integers using the randint function and print the average of the non-negative integers.
# Tip: Zero is considered a non-negative integer

# from random import randint
# print(sum(x := [i for i in [randint(-100, 100) for i in range(6)] if i >= 0]) / len(x))

# Create a variable to store the string "20 30 100". Write code to add the numbers in the string to print their total on
# the shell.

# print((s := "20 30 100") * 0, sum([int(i) for i in s.split()]), sep="")

# Write a program that generates a tuple of three random integers. Use the random module to print a random element from
# the tuple without using the choice function.

# from random import randint
# print(tuple(randint(1, 100) for i in range(3))[randint(0, 2)])

# Ask the user to enter a floating point number (e.g. 3.15) and print the digits after the decimal point in reverse
# order.
# For example:
# Please enter a floating point number: 3.15
# Output: 51

# print((f := str(float(input("Enter a float: "))))[f.index(".") + 1:][::-1])

# Create the following lists:
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# fruits = ["Apple", "Banana", "Pear", "Apple", "Pineapple", "Apple", "Pear", "Guava", "Grapes", "Watermelon"]
# Write code to generate a dictionary such that each number is a key and the corresponding fruit in the other list
# becomes its value. Print the generated dictionary.

# print({key: value for key, value in zip([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ["Apple", "Banana", "Pear", "Apple", "Pineapple", "Apple", "Pear", "Guava", "Grapes", "Watermelon"])})

# Create a list as shown below:
# numbers = [[20, 3, 23], [34, 2, 34],[56, 456, 12]]
# Write code to print the average of all these numbers.

# print(sum(x := [n for number in [[20, 3, 23], [34, 2, 34], [56, 456, 12]] for n in number]) / len(x))

# Create a dictionary that contains four names as keys and ages as values. Write code to print only those names whose
# age is an even number.

# [print(key) for key, value in {"Aarav": 10, "Aarin": 13, "Komal": 39, "Hemal": 46}.items() if value % 2 == 0]


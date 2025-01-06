# Abstract
A Basic JSON Parser made using Python. Uses a stream of tokens to convert into a Parse Tree. Has a built in error checking for semantic errors.

# Detected Errors
## 1. Invalid Decimal Format:
I coded my program to throw an error when a decimal number is incorrectly formatted, such as missing digits after the decimal point.
## 2. Empty Keys Not Allowed:
My program disallows empty keys in objects, as they don't make sense semantically and are invalid in JSON.
## 3. Invalid Number Format:
I added checks to ensure that numbers are formatted correctly. For example, leading + signs or multiple decimal points are flagged as errors.
## 4. Leading Zeros Not Allowed:
I disallow numbers with leading zeros (e.g., 0123), as they can be confusing and are generally not valid in standard JSON notation.
## 5. Reserved Word Usage:
JSON reserves certain words like true, which cannot be used as keys. My program flags them if they're used improperly.
## 6. Duplicate Keys:
Since JSON doesn’t allow duplicate keys, my program throws an error whenever it detects a key that appears more than once in an object.
## 7. Array Type Consistency:
Arrays must contain elements of the same type. My program throws an error if it detects a mix of different types, such as numbers and strings.
## 8. Reserved Word as String Value:
I disallow reserved words like true being used as string values, as this could lead to confusion and is not allowed in JSON.


# Compilation:
![image](https://github.com/user-attachments/assets/df956dba-e261-4ed9-a1c5-0aabaca76942)

# Author:  
Zawad Atif  
Zawad.Atif@dal.ca

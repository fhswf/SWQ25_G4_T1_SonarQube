def is_not_empty(value):
    if not value:
        return False
    else:
        return True

def main():
    # Input
    name = input("Enter your name: ")

    # Check if name is empty
    if is_not_empty(name):
        print("Hello, {}!".format(name))
    else:
        print("Name is empty.")

if __name__ == "__main__":
    main()

def fun(a):
  i = 10
  return i + a       # Noncompliant


def fun(b):
  i = 10
  return i + b       # Noncompliant

def fun(c):
  i = 10
  return i + c       # Noncompliant

def fun(d):
  i = 10
  return i + d      # Noncompliant

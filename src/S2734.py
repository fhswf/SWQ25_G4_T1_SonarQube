class MyClass(object):
    def __init__(self):
        self.message = 'Hello'
        # Noncompliant: a TypeError will be raised



if a != 2:        # Noncompliant
    b = i >= 10    # Noncompliant




from typing import List

def search_first_number_without_break(elements: List[str]):
    for elt in elements:
        if elt.isnumeric():
            return elt

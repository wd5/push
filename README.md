# Pymail

A command line interface to Gmail.


## Use

```python

p = Pymail()

p.login("user@gmail.com", "password")

p.select_folder("inbox")

print(p.messages_from("owain@owainlewis.com"))

```
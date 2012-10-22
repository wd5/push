# Pymail

A command line interface to Gmail.

![](https://raw.github.com/owainlewis/pymail/master/preview.png)

## Use

From the terminal

```python
python pymail.py -u yourname@gmail.com -p password

```

## API

```python

p = Pymail()

p.login("user@gmail.com", "password")

p.select_folder("inbox")

print(p.messages_from("owain@owainlewis.com"))

```
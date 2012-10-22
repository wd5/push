# Push

A command line interface to Gmail.

![](https://raw.github.com/owainlewis/pymail/master/preview.png)

## Use

From the terminal

```python
python push.py -u yourname@gmail.com -p password

```

## API

```python

p = Push()

p.login("user@gmail.com", "password")

p.select_folder("inbox")

print(p.messages_from("owain@owainlewis.com"))

```
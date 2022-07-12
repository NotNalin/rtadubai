# rtadubai
Unofficial API for RTA (Dubai)

## Installing

```bash
pip install rtadubai
```

## Examples

### Getting Nol Card balance

```python
from rtadubai import Nol

card = Nol.Card("Your nol card number")
balance = card.balance

# --------------------OR----------------------------

details = Nol.details("Your nol card number")
balance = details["balance"]
```

[More examples](https://github.com/NotNalin/rtadubai/tree/main/example)


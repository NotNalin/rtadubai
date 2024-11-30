# rtadubai [UNMAINTAINED]
Unofficial API for RTA (Dubai)

> [!WARNING]  
>  
> This library is no longer maintained, because:  
> 1. Most features don't work anymore.  
> 2. salik.ae is protected with Cloudflare, blocking any web scraping attempts.  
> 3. rta.ae now verifies the `g-recaptcha-response` field in requests, stopping web scraping.  
> 4. This was for a school project, and I no longer have a use for it or the time to maintain it.  
>  
> If you have any questions, feel free to contact me.  

## Installing

```bash
pip install rtadubai
```
## Installing Development Version

```bash
pip install git+https://github.com/NotNalin/rtadubai
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


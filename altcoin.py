from binance.client import Client
import pandas as pd
import time
client = Client("1nP6bqPkQJXte3dKtx3yQz0yBUyQJnMsJ6EaXHh3qF3IwB1pDkGdQddSZzV41WAL", "ydWMSGJRC5ONLZ8NqRTP0UXK6cOpirXjFuuROEf0cs6QckVZonURReyERhAdADZb")
x= pd.DataFrame(client.get_ticker())
print(x)
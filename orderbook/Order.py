class Order:
    id = 0
    price = 0
    time = 0
    volume = 0
    type = 0
    direction = 0

    def __init__(self, id, price, time, volume, type, direction):
        self.id = id
        self.price = price
        self.time = time
        self.volume = volume
        self.type = type
        self.direction = direction


class Order:
    order_id = 0
    visible_size = 0
    side = 0
    total_qty = 0
    executed_qty = 0
    order_qty = 0
    execution_type = 0
    transact_time = 0
    value = 0
    executed_value = 0
    broker_id = 0
    instrument_id = 0

    def __init__(self, order_id, visible_size, side, total_qty, executed_qty, order_qty,execution_type,transact_time,value,executed_value,broker_id,instrument_id):
        self.order_id = order_id
        self.visible_size = visible_size
        self.side = side
        self.total_qty = total_qty
        self.executed_qty = executed_qty
        self.order_qty = order_qty
        self.execution_type = execution_type
        self.transact_time = transact_time
        self.value = value
        self.executed_value = executed_value
        self.broker_id = broker_id
        self.instrument_id = instrument_id


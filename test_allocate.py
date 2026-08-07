from model import Batch,OrderLine,Quantity,Sku,Reference,allocate
from datetime import date, timedelta

# Since we "wrapped our parameters of the batch class" i.e created new units with NewType ,
# we need to use these units in all of examples

ref01 = Reference("in-stock-batch")
sku01 = Sku("RETRO-CLOCK")
qty01 = Quantity(100)

ref02 = Reference("shipment-batch")
today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch(ref01, sku01, qty01, eta=None)
    shipment_batch = Batch(ref02, sku01, qty01, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


sku_minimalist = Sku("MINIMALIST-SPOON")
ref_speedy = Reference("speedy-batch")
ref_normal = Reference("normal-batch")
ref_slow =  Reference("slow-batch")

def test_prefers_earlier_batches():

    earliest = Batch(ref_speedy, sku_minimalist, qty01, eta=today)
    medium = Batch(ref_normal, sku_minimalist, qty01, eta=tomorrow)
    latest = Batch(ref_slow, sku_minimalist, qty01, eta=later)

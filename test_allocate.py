from model import Batch,OrderLine,Quantity,Sku,Reference,allocate,OutOfStock
from datetime import date, timedelta
import pytest

# Since we "wrapped our parameters of the batch class" i.e created new units with NewType ,
# we need to use these units in all of examples

ref01 = Reference("in-stock-batch")
sku01 = Sku("RETRO-CLOCK")
qty01 = Quantity(100)
qty01 = Quantity(10)
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
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100

ref_in_stock = Reference("in-stock-batch-ref")
sku_poster01 = Sku("HIGHBROW-POSTER")
ref_shipment = Reference("shipment-batch-ref")

def test_returns_allocated_batch_ref():

    in_stock_batch = Batch(ref_in_stock, sku_poster01, qty01,
    eta=None)
    shipment_batch = Batch(ref_shipment, sku_poster01, qty01,
    eta=tomorrow)

    line = OrderLine("oref", sku_poster01, 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference

ref_batch1 = Reference('batch1')
sku_small_fork = Sku('SMALL-FORK')

def test_raises_out_of_stock_exception_if_cannot_allocate():

    batch = Batch(ref_batch1,sku_small_fork , qty01, eta=today)

    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    with pytest.raises(OutOfStock, match='SMALL-FORK'):

        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])


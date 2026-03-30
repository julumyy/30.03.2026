from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is 0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0

    costs = manager.get_apartment_costs('apart-polanka', najemcy=2)
    assert costs == 1766.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, najemcy=3)
    assert costs == 457.0  

    costs = manager.get_apartment_costs('apart-polanka', najemcy=0)
    assert costs == None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1, najemcy=2)
    assert costs == 111.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1, najemcy=1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0
    
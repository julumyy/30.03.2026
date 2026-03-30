import pytest

from pydantic import ValidationError
from src import manager
from src.models import Apartment, Parameters, Tenant
from src.models import ApartmentSettlement
from src.manager import Manager

def test_apartment_fields():
    data = Apartment(
        key="apart-test",
        name="Test Apartment",
        location="Test Location",
        area_m2=50.0,
        rooms={
            "room-1": {"name": "Living Room", "area_m2": 30.0},
            "room-2": {"name": "Bedroom", "area_m2": 20.0}
        }
    )
    assert data.key == "apart-test"
    assert data.name == "Test Apartment"
    assert data.location == "Test Location"
    assert data.area_m2 == 50.0
    assert len(data.rooms) == 2


def test_apartment_from_dict():
    data = {
        "key": "apart-test",
        "name": "Test Apartment",
        "location": "Test Location",
        "area_m2": 50.0,
        "rooms": {
            "room-1": {"name": "Living Room", "area_m2": 30.0},
            "room-2": {"name": "Bedroom", "area_m2": 20.0}
        }
    }
    apartment = Apartment(**data)
    assert apartment.key == data["key"]
    assert apartment.name == data["name"]
    assert apartment.location == data["location"]
    assert apartment.area_m2 == data["area_m2"]
    assert len(apartment.rooms) == len(data["rooms"])

    data['area_m2'] = "25m2" # Invalid field
    with pytest.raises(ValidationError):
        wrong_apartment = Apartment(**data)

def test_tenant_fields():
    tenant = Tenant(
        name='Test Tenant',
        apartment='apart-test',
        room='test-room',
        apartment_key='apart-test',
        rent_pln=1500.0,
        deposit_pln=3000.0,
        date_agreement_from='2024-01-01',
        date_agreement_to='2024-12-31'
    )

    assert tenant.name == 'Test Tenant'
    assert tenant.apartment == 'apart-test'
    assert tenant.room == 'test-room'
    assert tenant.apartment == 'apart-test'
    assert tenant.rent_pln == 1500.0
    assert tenant.deposit_pln == 3000.0
    assert tenant.date_agreement_from == '2024-01-01'
    assert tenant.date_agreement_to == '2024-12-31'

def test_tenant_from_dict():
    data = {
        "name": "Test Testowy",
        "apartment": "test-apart",
        "room": "test-room",
        "rent_pln": 4324.0,
        "deposit_pln": 12356.0,
        "date_agreement_from": "2032-01-01",
        "date_agreement_to": "2033-01-01"
    }
    tenant = Tenant(**data)
    assert tenant.name == data["name"]
    assert tenant.apartment == data["apartment"]
    assert tenant.room == data["room"]
    assert tenant.rent_pln == data["rent_pln"]

    with pytest.raises(ValidationError):
        data['rent_pln'] = "1500PLN" # Invalid field
        wrong_tenant = Tenant(**data)

def test_apartment_settlement_logic():

    manager = Manager(Parameters())
    apartment_id = "apart-polanka"
    settlement = manager.create_apartment_settlement(apartment_id, month=1, year=2025)

    assert settlement.apartment == apartment_id
    assert settlement.month == 1
    assert settlement.year == 2025

    assert settlement.total_bills_pln == 910.0   
    assert settlement.total_rent_pln == 1150.0
    assert settlement.total_due_pln == 910.0
    assert isinstance(settlement.total_due_pln, float)

    empty_settlement = manager.create_apartment_settlement("apart-empty", month=1, year=2025)

    assert empty_settlement.total_due_pln == 0.0
    assert empty_settlement.total_bills_pln == 0.0
    assert empty_settlement.apartment == "apart-empty"

def test_should_create_list_of_tenant_settlements():

    manager = Manager(Parameters())
    apt_settlement = ApartmentSettlement(
        apartment="apart-polanka",
        month=1,
        year=2024,
        total_rent_pln=0.0,
        total_bills_pln=1372.0,
        total_due_pln=1372.0
    )

    tenants=["Nowak", "Kowalski", "Adamska"]

    results = manager.create_tenant_settlements(apt_settlement, tenants)

    assert len(results) == 3
    assert results[0].tenant == "Nowak"
    assert results[1].tenant == "Kowalski" 
    assert results[2].tenant == "Adamska"  
    #assert results[1].bills_pln == 1372.0
    assert results[0].bills_pln == 1372.0
    assert results[0].month == apt_settlement.month
    assert results[0].year == apt_settlement.year
    assert results[0].apartment_settlement == apt_settlement.apartment
    assert isinstance(results[0].bills_pln, float)
    assert results[0].total_due_pln == 1372.0
    assert results[0].balance_pln == -1372.0
from src.models import Apartment, Bill, Parameters, Tenant, TenantSettlement, Transfer
from src.models import ApartmentSettlement

class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    
    def get_apartment_costs(self, apartment_key, year=None, month=None, najemcy=1):
        total = 0
        #apartments = Apartment.from_json_file(parameters.apartments_json_path)
        for bill in self.bills:
            if apartment_key == bill.apartment:
                if year == bill.settlement_year or not year:
                    if month == bill.settlement_month or not month:
                        total += bill.amount_pln
        
        if najemcy > 1:
            total /= najemcy
            total = round(total)
        elif najemcy < 1:
            total = None
        return total
        
    def create_apartment_settlement(self, apartment_id, month, year):
        bills_sum = self.get_apartment_costs(apartment_id, year, month, najemcy=1)
        
        total_bills = bills_sum if bills_sum is not None else 0.0
        
        return ApartmentSettlement(
            apartment=apartment_id,
            month=month,
            year=year,
            total_rent_pln=1150.0,
            total_bills_pln=total_bills,
            total_due_pln=total_bills
            )
        
    def create_tenant_settlements(self, apartment_settlement, tenants):
        if not tenants:
            return []
        
        tenant_settlements = []
        
        for tenant in tenants:
            tenant_settlement = TenantSettlement(
                tenant=tenant,
                apartment_settlement=apartment_settlement.apartment,
                month=apartment_settlement.month,
                year=apartment_settlement.year,
                rent_pln=apartment_settlement.total_rent_pln,
                bills_pln=apartment_settlement.total_bills_pln,
                total_due_pln=apartment_settlement.total_due_pln,
                balance_pln=-apartment_settlement.total_due_pln
            )
            tenant_settlements.append(tenant_settlement)
        return tenant_settlements
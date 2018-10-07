package my.dummy.project4.api;

import my.dummy.project5.domain.Bill;
import my.dummy.project5.domain.Deptor;

public interface IBillingService {
				
	String getMoney(Deptor deptor, Bill bill, boolean gready); 

}

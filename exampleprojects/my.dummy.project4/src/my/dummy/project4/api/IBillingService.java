package my.dummy.project4.api;

import my.dummy.project1.api.IDummy;
import my.dummy.project4.util.BillingUtil;
import my.dummy.project5.domain.Bill;
import my.dummy.project5.domain.Deptor;

public interface IBillingService extends IDummy {
				
	String getMoney(Deptor deptor, Bill bill, boolean gready, BillingUtil util); 

}

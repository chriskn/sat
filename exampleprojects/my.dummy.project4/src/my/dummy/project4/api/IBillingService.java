package my.dummy.project4.api;

import org.eclipse.xtext.formatting.IElementMatcherProvider.IBetweenElements;

import my.dummy.project5.domain.*;

public interface IBillingService extends IBetweenElements {
				
	String getMoney(Deptor deptor, Bill bill, boolean gready); 

}

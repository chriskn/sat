package my.dummy.project4.impl;

import org.eclipse.xtext.AbstractElement;
import org.eclipse.xtext.util.Pair;

import my.dummy.project4.api.IBillingService;
import my.dummy.project5.domain.Bill;
import my.dummy.project5.domain.Deptor;

public class BillingService implements IBillingService {

	@Override
	public String getMoney(Deptor deptor, Bill bill, boolean gready) {
		return null;
	}

	@Override
	public Pair<AbstractElement, AbstractElement> matchBetween() {
		return null;
	}

}

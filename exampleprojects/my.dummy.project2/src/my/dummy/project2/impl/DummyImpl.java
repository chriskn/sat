package my.dummy.project2.impl;

import java.util.Observable;
import java.util.Observer;

import my.dummy.project1.api.AbstractDummy;
import my.dummy.project1.api.IDummy;

public class DummyImpl extends AbstractDummy implements IDummy, Observer {
	
	public boolean trigger; 
	private int number; 
	IDummy dummy; 
	
	private int addOther(int other) {
		return number+other; 
	}

	@Override
	public void update(Observable o, Object arg) {
	}

	@Override
	public void remove() {
		// TODO Auto-generated method stub
		
	}
}

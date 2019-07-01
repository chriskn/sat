package my.dummy.project3.impl;

import my.dummy.project1.api.AbstractDummy;
import my.dummy.project1.impl.ClassInSplitPackage;


public class ClassUsingClassFromSplitPackage {

	ClassInSplitPackage cisp; 
	AbstractDummy dummy; 
	
	public boolean test(String blub) {
		return blub.equals("");
	}

}

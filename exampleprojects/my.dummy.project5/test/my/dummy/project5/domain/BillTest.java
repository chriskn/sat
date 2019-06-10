package my.dummy.project5.domain;

import org.junit.Test;

public class BillTest {

	
	@Test
	public void test() {
		Bill sut = new Bill("","", State.CREATED);
		sut.hashCode(); 
	}
}

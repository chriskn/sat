package my.dummy.project5.domain;

import org.junit.Test;

public class DeptorTest {

	
	@Test
	public void test() {
		Deptor sut = new Deptor("", "", "", 12345); 
		sut.hashCode(); 
	}
}

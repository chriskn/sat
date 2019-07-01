package my.dummy.project1.api;

public abstract class AbstractDummy {
	
	private static String name = AbstractDummy.class.getName(); 

	public abstract void remove(); 
	
	protected String getName() {
		return name;
	}
	
}

public class ComplDummy {

	private static String complExample1(String antPattern, String directorySeparator) {
		final String escapedDirectorySeparator = '\\' + directorySeparator;
		final StringBuilder sb = new StringBuilder(antPattern.length());
		sb.append('^');
		int i = antPattern.startsWith("/") || // +1
				antPattern.startsWith("\\") ? 1 : 0; // +1
		while (i < antPattern.length()) { // +1
			final char ch = antPattern.charAt(i);
			if ("".indexOf(ch) != -1) { // +2 (nesting = 1)
				sb.append('\\').append(ch);
			} else if (ch == '*') { // +1
				if (i + 1 < antPattern.length() // +3 (nesting = 2)
						&& antPattern.charAt(i + 1) == '*') { // +1
					if (i + 2 < antPattern.length() // +4 (nesting = 3)
							&& isSlash(antPattern.charAt(i + 2))) { // +1
						sb.append("(?:.*").append(escapedDirectorySeparator).append("|)");
						i += 2;
					} else { // +1
						sb.append(".*");
						i += 1;
					}
				} else { // +1
					sb.append("[^").append(escapedDirectorySeparator).append("]*?");
				}
			} else if (ch == '?') { // +1
				sb.append("[^").append(escapedDirectorySeparator).append("]");
			} else if (isSlash(ch)) { // +1
				sb.append(escapedDirectorySeparator);
			} else { // +1
				sb.append(ch);
			}
			i++;
		}
		sb.append('$');
		return sb.toString();
	} // Cognitive Complexity 20

	private void complExample2(final Entry entry, final Transaction txn)
			throws PersistitInterruptedException, RollbackException {
		Entry _persistit = null;
		final TransactionIndex ti = _persistit.getTransactionIndex();
		while (true) { // +1
			try {
				synchronized (this) {
					Entry frst = null;
					if (frst != null) { // +2 (nesting = 1)
						if (frst.getVersion() > entry.getVersion()) { // +3 (nesting = 2)
							throw new RollbackException();
						}
						if (txn.isActive()) { // +3 (nesting = 2)
							for // +4 (nesting = 3)
							(Entry e = frst; e != null; e = e.getPrevious()) {
								final long version = e.getVersion();
								final long depends = ti.wwDependency(version, txn.getTransactionStatus(), 0);
								if (depends == TIMED_OUT) { // +5 (nesting = 4)
									throw new WWRetryException(version);
								}
								if (depends != 0 // +5 (nesting = 4)
										&& depends != ABORTED) { // +1
									throw new RollbackException();
								}
							}
						}
					}
					entry.setPrevious(frst);
					frst = entry;
					break;
				}
			} catch (final WWRetryException re) { // +2 (nesting = 1)
				try {
					final long depends = _persistit.getTransactionIndex().wwDependency(re.getVersionHandle(),
							txn.getTransactionStatus(), SharedResource.DEFAULT_MAX_WAIT_TIME);
					if (depends != 0 // +3 (nesting = 2)
							&& depends != ABORTED) { // +1
						throw new RollbackException();
					}
				} catch (final InterruptedException ie) { // +3 (nesting = 2)
					throw new PersistitInterruptedException(ie);
				}
			} catch (final InterruptedException ie) { // +2 (nesting = 1)
				throw new PersistitInterruptedException(ie);
			}
		}
	} // Cognitive Complexity 35

	private MethodJavaSymbol complExample3(ClassJavaType classType) {
		if (classType.isUnknown()) { // +1
			return Symbols.unknownMethodSymbol;
		}
		boolean unknownFound = false;
		List<JavaSymbol> symbols = classType.getSymbol();
		for (JavaSymbol overrideSymbol : symbols) { // +1
			if (overrideSymbol.isKind(JavaSymbol.MTH) // +2 (nesting = 1)
					&& !overrideSymbol.isStatic()) { // +1
				MethodJavaSymbol methodJavaSymbol = (MethodJavaSymbol) overrideSymbol;
				if (canOverride(methodJavaSymbol)) { // +3 (nesting = 2)
					Boolean overriding = checkOverridingParameters(methodJavaSymbol, classType);
					if (overriding == null) { // +4 (nesting = 3)
						if (!unknownFound) { // +5 (nesting = 4)
							unknownFound = true;
						}
					} else if (overriding) { // +1
						return methodJavaSymbol;
					}
				}
			}
		}
		if (unknownFound) { // +1
			return Symbols.unknownMethodSymbol;
		}
		return null;
	} // total complexity = 19

	private void doWhileExample(){
		int i = 0;
		do { //1
			if (true) { //2
				i++;
			}
		} while(i < 10);
	} // Cognitive Complexity 3
	
	private boolean complExample4(State state, String value, String matchCondition) {
        boolean matched = false;
        String unquotedValue = value;
        if (unquotedValue.startsWith("\"") && unquotedValue.endsWith("\"")) { 
            unquotedValue = unquotedValue.substring(1, unquotedValue.length() - 1);
        }
        Condition condition = Condition.EQUAL;
        if (matchCondition != null) { 
            condition = Condition.fromString(matchCondition);
            if (condition == null) { 
                logger.warn("matchStateToValue: unknown match condition '{}'", matchCondition);
                return matched;
            }
        }
        if (unquotedValue.equals(UnDefType.NULL.toString()) || unquotedValue.equals(UnDefType.UNDEF.toString())) { // +2
            switch (condition) { 
                case EQUAL:
                    if (unquotedValue.equals(state.toString())) { 
                        matched = true;
                    }
                    break;
                case NOT:
                case NOTEQUAL:
                    if (!unquotedValue.equals(state.toString())) { 
                        matched = true;
                    }
                    break;
                default:
                    break;
            }
        } else { 
            if (state instanceof DecimalType || state instanceof QuantityType<?>) { 
                try {
                    double compareDoubleValue = Double.parseDouble(unquotedValue);
                    double stateDoubleValue;
                    if (state instanceof DecimalType) { 
                        stateDoubleValue = ((DecimalType) state).doubleValue();
                    } else { //+1
                        stateDoubleValue = ((QuantityType<?>) state).doubleValue();
                    }
                    switch (condition) { 
                        case EQUAL:
                            if (stateDoubleValue == compareDoubleValue) {
                                matched = true;
                            }
                            break;
                        case LTE:
                            if (stateDoubleValue <= compareDoubleValue) {
                                matched = true;
                            }
                            break;
                        case GTE:
                            if (stateDoubleValue >= compareDoubleValue) {
                                matched = true;
                            }
                            break;
                        case GREATER:
                            if (stateDoubleValue > compareDoubleValue) { 
                                matched = true;
                            }
                            break;
                        case LESS:
                            if (stateDoubleValue < compareDoubleValue) { 
                                matched = true;
                            }
                            break;
                        case NOT:
                        case NOTEQUAL:
                            if (stateDoubleValue != compareDoubleValue) { 
                                matched = true;
                            }
                            break;
                    }
                } catch (NumberFormatException e) { 
                    logger.debug("matchStateToValue: Decimal format exception: ", e);
                }
            } else if (state instanceof DateTimeType) { 
                ZonedDateTime val = ((DateTimeType) state).getZonedDateTime();
                ZonedDateTime now = ZonedDateTime.now();
                long secsDif = ChronoUnit.SECONDS.between(val, now);
                try {
                    switch (condition) { 
                        case EQUAL:
                            if (secsDif == Integer.parseInt(unquotedValue)) {
                                matched = true;
                            }
                            break;
                        case LTE:
                            if (secsDif <= Integer.parseInt(unquotedValue)) {
                                matched = true;
                            }
                            break;
                        case GTE:
                            if (secsDif >= Integer.parseInt(unquotedValue)) {
                                matched = true;
                            }
                            break;
                        case GREATER:
                            if (secsDif > Integer.parseInt(unquotedValue)) { 
                                matched = true;
                            }
                            break;
                        case LESS:
                            if (secsDif < Integer.parseInt(unquotedValue)) { 
                                matched = true;
                            }
                            break;
                        case NOT:
                        case NOTEQUAL:
                            if (secsDif != Integer.parseInt(unquotedValue)) { 
                                matched = true;
                            }
                            break;
                    }
                } catch (NumberFormatException e) { 
                    logger.debug("matchStateToValue: Decimal format exception: ", e);
                }
            } else { 
                switch (condition) {
                    case NOT:
                    case NOTEQUAL:
                        if (!unquotedValue.equals(state.toString())) { 
                            matched = true;
                        }
                        break;
                    default:
                        if (unquotedValue.equals(state.toString())) { 
                            matched = true;
                        }
                        break;
                }
            }
        }

        return matched;
    } // Cognitive Complexity 96

	private	String switchExample(int number) {    
		switch (number) {         // +1      
		  case 1: return "one";
		  case 2: return "a couple";
		  case 3: return "a few";
		  default: return "lots";
		}  
	} // Cognitive Complexity 1

	private int ifInLoops(int max) {   
	  int total = 0;
	  for (int i = 1; i <= max; ++i) { 		// +1    
		for (int j = 2; j < i; ++j) {       // +2      
			if (i % j == 0) {               // +3        
				System.out.println("foo");        
			}    
		}    
		total += i;
	  }  
	  return total;
	} // Cognitive Complexity 6

	private static String ifElseifExample(int in){
		while(true){ //1
			if(in ==0){ //2
			}else if(in ==1){ //1
			}else { //1
			}
		}
	} // Cognitive Complexity 5

}

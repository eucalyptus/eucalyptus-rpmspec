#!/bin/sh

CLASSPATH="/usr/share/java/*:${CLASSPATH}" java org.apache.axis2.wsdl.WSDL2C $*

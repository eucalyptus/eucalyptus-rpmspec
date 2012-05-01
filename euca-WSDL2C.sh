#!/bin/sh

CLASSPATH=$(build-classpath axis2 backport-util-concurrent commons-logging ws-commons-axiom ws-commons-XmlSchema ws-commons-neethi wsdl4j xalan-j2 xsltc) java org.apache.axis2.wsdl.WSDL2C $*

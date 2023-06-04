#!/usr/bin/env python3

import socket
import sys
import argparse
import random
import re
import pprint
import time
import logging
import os

class Event:
	def socketClient(self):
		mySocketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#probeHost = "HPZR6NOIOMIMB"
		probeHost = "9.185.151.168"
		probePort = 4567
		mySocketClient.connect((probeHost,probePort))
		return mySocketClient
	def __init__(self):
		self.NetworkStatus = {'RouterA': 2, 'RouterB':2,'RouterC':2}
		self.ComputerAllNode = ["HostA","HostA2","HostB","HostC"]
		self.ComputerAllComponent = ["CPU","DISK","Memory"]
		self.ComputerStatus = {'HostA':[{'CPU': 2},{'DISK':2},{'Memory':2},{'Power':2}],
				       'HostA2':[{'CPU': 2},{'DISK':2},{'Memory':2},{'Power':2}],
				       'HostB':[{'CPU': 2},{'DISK':2},{'Memory':2},{'Power':2}],
				       'HostC':[{'CPU': 2},{'DISK':2},{'Memory':2},{'Power':2}]}
		self.ComputerEvents = {'CPU':{'AG':'HarwareStatus','AK':'ProcessorM','PSummary':'CPU 2 offline','RSummary':'CPU 2 online','Manager':'UA','Agent':'Director','Sev':'3','EventId':'CPUStatus'},
				       'DISK':{'AG':'HarwareStatus','AK':'DSIKM','PSummary':'Disk failure','RSummary':'Disk go back','Manager':'UA','Agent':'Director','Sev':'5','EventId':'DiskStatus'},
				       'Memory':{'AG':'HarwareStatus','AK':'MemoryM','PSummary':'Memory Error','RSummary':'Memory OK','Manager':'UA','Agent':'Director','Sev':'4','EventId':'RAMStatus'},
				       'Power':{'AG':'PowerSupply','AK':'PowerVoltage','PSummary':'Power vaoltage low','RSummary':'Power vaoltage normal','Manager':'UA','Agent':'Director','Sev':'3','EventId':'PowerVoltage'}}

		self.ApplicationNodeStatus = {'Beijing':2,'Sydney':2,'NewYork':2,'London':2}
		self.ApplicationAllNode = ["Beijing","Sydney","NewYork","London"]
		self.ApplicationAllEvent =["WebServer","Database","App"]
		self.AppEvents = {'WebServer':{'AG':'WebApplication','AK':'WAStatus','PSummary':'Web Portal not avaiable','RSummary':'Web Portal avaiable','Manager':'Tivoli','Agent':'Scaner','Sev':'5','EventId':'WebStatus'},
				  'Database':{'AG':'Database','AK':'DB Engine','PSummary':'Database down','RSummary':'Database up','Manager':'EIF','Agent':'DBAgent','Sev':'5','EventId':'DBStatus'},
				  'App':{'AG':'Application','AK':'ProcessorM','PSummary':'App not response','RSummary':'App responsed','Manager':'OPV','Agent':'Detect','Sev':'5','EventId':'APPStatus'}}
		self.AppProvision = {"Beijing":'Database',"Sydney":'App',"NewYork":'Database',"London":'WebServer'}
		###self.aSC = self.socketClient()
		#AlarmFormat : Node@@AlertGroup@@AlertKey@@Summary@@Manager@@Agent@@Severity@@Type@@EventID
	def sendEvent(self,aSC,msgToBeSent):
		aSC.send(msgToBeSent)
		data = aSC.recv(1024)
		logging.debug(data)
		

	def EventG(self,Node,EventIndex,Type,EventsList):
		msgG = ''
		if Type == 1 :
			msgG = Node + '@@' +  EventsList[EventIndex]['AG'] + "@@" +EventsList[EventIndex]['AK'] + "@@" +EventsList[EventIndex]['PSummary'] + "@@" + EventsList[EventIndex]['Manager'] + "@@" + EventsList[EventIndex]['Agent'] + "@@" + EventsList[EventIndex]['Sev'] + "@@" + str(1) + "@@" + EventsList[EventIndex]['EventId'] + "\n"
		elif Type == 2:
			msgG = Node + '@@' +  EventsList[EventIndex]['AG'] + "@@" +EventsList[EventIndex]['AK'] + "@@" +EventsList[EventIndex]['RSummary'] + "@@" + EventsList[EventIndex]['Manager'] + "@@" + EventsList[EventIndex]['Agent'] + "@@" + str(1) + "@@" + str(2) + "@@" + EventsList[EventIndex]['EventId'] + "\n"
		elif Type == 13:
			msgG = Node + '@@' +  EventsList[EventIndex]['AG'] + "@@" +EventsList[EventIndex]['AK'] + "@@" +EventsList[EventIndex]['ISummary'] + "@@" + EventsList[EventIndex]['Manager'] + "@@" + EventsList[EventIndex]['Agent'] + "@@" + str(2) + "@@" + str(13) + "@@" + EventsList[EventIndex]['EventId'] + "\n"
		else:
			logging.error("Type not recognized")
			sys.exit(2)
		return(msgG)

class NEvent(Event):
	aMsg = 'Welcome to NEvents'
	def __init__(self):
		self.number = 0
		self.Var = 0
		self.EventNode = ['Sydney','Roma','London','Paris','Berlin','Moscow','Beijing','Tokoy','New Delhi','New York','Sao Paulo','Cairo']
		self.Events = {}
		self.EventStatus = {}
		Event.__init__(self)
	def initEvents(self,aVar):
		index = 0
		for i in range(0,len(self.EventNode)):
			for k in range(0,int(aVar)):
				Sev = random.randint(2,5)
				self.Events[index] = {}
				self.Events[index]['Node'] = self.EventNode[i]
				self.Events[index]['AG'] = 'SIMAG' + str(k)
				self.Events[index]['AK'] = 'SIMAK' + str(k)
				self.Events[index]['PSummary'] = 'Problem on ' + 'SIMAG'+str(k) + 'SIMAK' + str(k)
				self.Events[index]['RSummary'] = 'Resolution on ' + 'SIMAG'+str(k) + 'SIMAK' + str(k) 
				self.Events[index]['Manager'] = 'SocketProbeS'
				self.Events[index]['Agent'] = 'Python'
				self.Events[index]['Sev'] = str(Sev)
				self.Events[index]['EventId'] = 'SIM' + str(i*k)

				self.EventStatus[index] = 2

				index += 1
	
	def NEventG(self):
		logging.info("Now Starting genreate Random event " + self.number + " times")
		mySC = self.socketClient()
		i = 0
		while i < int(self.number):
			NodeIndex = random.randint(0,len(self.EventNode)-1)
			EventType = random.randint(1,2)
			Node = self.Events[NodeIndex]['Node']
			msgStream = self.EventG(Node,NodeIndex,EventType,self.Events)
			logging.debug("sending : " + msgStream)
			self.sendEvent(mySC,msgStream)
			time.sleep(300)
			i += 1
		logging.info(i + " events sent")
		mySC.close()

class SEvent(Event):
	aMsg = 'Welcome to SEvents'
	def __init__(self):
		self.aEvent = ""
		Event.__init__(self)
	
	#AlarmFormat : Node@@AlertGroup@@AlertKey@@Summary@@Manager@@Agent@@Severity@@Type@@EventID 
	mySEvent = {'A':{'Node':'Maroubra','AG':'Traffic','AK':'Light','PSummary':'Stop working','RSummary':'Start working','Manager':'TMonitor','Agent':'Passenger','Sev':'4','EventId':'TrafficLight'},
		    'B':{'Node':'Eastlakes','AG':'Weather','AK':'Temperature','PSummary':'Too hot','RSummary':'Cool now','Manager':'WMonitor','Agent':'ThermalMeter','Sev':'3','EventId':'Feeling'},
		    'C':{'Node':'City','AG':'Security','AK':'StreetFighting','PSummary':'Gang fighting','RSummary':'Arrested','Manager':'SMonitor','Agent':'Police','Sev':'5','EventId':'Safety'},
		    'D':{'Node':'ConnellsPoint','AG':'Facility','AK':'StreetLight','PSummary':'Too dark','RSummary':'Bright now','Manager':'FMonitor','Agent':'Residence','Sev':'2','EventId':'StreetLight'},
		    'E':{'Node':'HunterHills','AG':'Event','AK':'Celebrate','PSummary':'Too noisy','RSummary':'Celebrate stopped','Manager':'EMonitor','Agent':'Council','Sev':'2','EventId':'EventActivity'}}
	def SEventG(self):
		logging.info("Now Starting genreate Seasonal event of  " + self.aEvent)
		mySC = self.socketClient()
		msgStream = self.mySEvent[self.aEvent]['Node'] + "@@" + self.mySEvent[self.aEvent]['AG'] + "@@" +self.mySEvent[self.aEvent]['AK'] + "@@" +self.mySEvent[self.aEvent]['PSummary'] + "@@" + self.mySEvent[self.aEvent]['Manager'] + "@@" + self.mySEvent[self.aEvent]['Agent'] + "@@" + self.mySEvent[self.aEvent]['Sev'] + "@@" + str(1) + "@@" + self.mySEvent[self.aEvent]['EventId'] + "\n"
		logging.debug("sending : " + msgStream)
		self.sendEvent(mySC,msgStream)
		time.sleep(3600)
		if self.aEvent != 'B':
			logging.debug("Now Starting genreate resolution Seasonal event of  " + self.aEvent)
			msgStream = self.mySEvent[self.aEvent]['Node'] + "@@" + self.mySEvent[self.aEvent]['AG'] + "@@" +self.mySEvent[self.aEvent]['AK'] + "@@" +self.mySEvent[self.aEvent]['RSummary'] + "@@" + self.mySEvent[self.aEvent]['Manager'] + "@@" + self.mySEvent[self.aEvent]['Agent'] + "@@" + str(1) + "@@" + str(2) + "@@" + self.mySEvent[self.aEvent]['EventId'] + "\n"
			logging.debug("sending : " + msgStream)
			self.sendEvent(mySC,msgStream)
		mySC.close()
		return


class REvents(Event):
	# Tuples
	EventType = ("Network","Computer","Application")
	# List
	NetworkAllNode = ["RouterA","RouterB","RouterC","RouterA1","RouterA2","RouterA3","RouterB1","RouterB2","RouterB3","RouterB4","RouterC1","RouterC2"]
	NetworkR = {'RouterA':{1:'RouterA1',2:'RouterA2',3:'RouterA3'},
		    'RouterB':{1:'RouterB1',2:'RouterB2',3:'RouterB3',4:'RouterB4'},
		    'RouterC':{1:'RouterC1',2:'RouterC2'}}
	#AlarmFormat : Node@@AlertGroup@@AlertKey@@Summary@@Manager@@Agent@@Severity@@Type@@EventID 
	NetworkEvent = {'AG':'Status','AK':'Link','Summary':'Link Down','Manager':'SNMPProbe','Agent':'MIB'}

	aMsg = 'Welcome to REvents'

	def __init__(self):
		self.number = 0
		Event.__init__(self)
		self.mySC = self.socketClient()

	def appEventG(self,aNode,aComponent):
		msgStream = 0
		if self.ApplicationNodeStatus[aNode] == 2:
			msgStream = self.EventG(aNode,aComponent,1,self.AppEvents)
			###logging.debug("sending Problem " + msgStream)
			###self.sendEvent(self.mySC,msgStream)
			self.ApplicationNodeStatus[aNode] = 1
		elif self.ApplicationNodeStatus[aNode] == 1:
			msgStream = self.EventG(aNode,aComponent,2,self.AppEvents)
			###logging.debug("sending Resolution " + msgStream)
			###self.sendEvent(self.mySC,msgStream)
			self.ApplicationNodeStatus[aNode] = 2
		else:
			logging.warning("Error uknown item status")
		return(msgStream)

	def appDBG(self,aNode):
		#Check peer side
		msgStream = self.appEventG(aNode,self.AppProvision[aNode])
		logging.debug("sending : " + msgStream)
		self.sendEvent(self.mySC,msgStream)
		logging.debug(self.AppProvision[aNode] + " on " + aNode + " : " + msgStream)
		if self.ApplicationNodeStatus[aNode] == 1:
			for Node,Dep in self.AppProvision.items():
				if Dep == "Database" and Node != aNode:
					if self.ApplicationNodeStatus[Node] == 2:
						logging.debug("Peer " + Dep + " on " + Node + " is available")
					elif self.ApplicationNodeStatus[Node] == 1:
						logging.debug("Peer " + Dep + " on " + Node + " is unavailable")
						for rNode,rDep in self.AppProvision.items():
							if rDep == 'App':
								self.ApplicationNodeStatus[rNode] == 2
								time.sleep(540)	
								self.appEventG(rNode,rDep)
								self.sendEvent(self.mySC,msgStream)

					else:
						logging.error("Unkown status of peer side")
		elif self.ApplicationNodeStatus[aNode] == 2:
			for Node,Dep in self.AppProvision.items():
				if Dep == "Database" and Node != aNode:
					self.ApplicationNodeStatus[Node] == 1
					time.sleep(540)	
					self.appEventG(Node,Dep)
					self.sendEvent(self.mySC,msgStream)
					if self.ApplicationNodeStatus[Node] == 2:
						logging.debug("Peer " + Dep + " on " + Node + " is available")
					elif self.ApplicationNodeStatus[Node] == 1:
						logging.debug("Peer " + Dep + " on " + Node + " is unavailable")
					else:
						logging.debug("Unkown status of peer side")
		else:
			logging.warning("Unkown status of peer side")
		

	def appWebG(self,aNode):
		aMsgStream = self.appEventG(aNode,self.AppProvision[aNode])
		logging.debug(self.AppProvision[aNode] + " on " + aNode + " : " + aMsgStream)
		self.sendEvent(self.mySC,msgStream)

	def appAPPG(self,aNode):
		aMsgStream = self.appEventG(aNode,self.AppProvision[aNode])
		logging.debug(self.AppProvision[aNode] + " on " + aNode + " : " + aMsgStream)
		self.sendEvent(self.mySC,msgStream)
		for Node,Dep in self.AppProvision.items():
			if Dep == 'WebServer':
				# Will trigger again anyway
				if self.ApplicationNodeStatus[aNode] == 1:
					# Will trigger again anyway
					self.ApplicationNodeStatus[Node] == 2
				elif self.ApplicationNodeStatus[aNode] == 2:
					self.ApplicationNodeStatus[Node] == 1
				time.sleep(480)	
				self.appWebG(Node)

	def AppG(self,aNode):
		logging.debug("Checking " + aNode)
		if self.AppProvision[aNode] == 'App':
			self.appAPPG(aNode)
		elif self.AppProvision[aNode] == 'WebServer':
			self.appWebG(aNode)
		elif self.AppProvision[aNode] == 'Database':
			self.appDBG(aNode)

	def computerEventG(self,aHost,aComponentId,aComponent):
		msgStream = 0
		if self.ComputerStatus[aHost][aComponentId][aComponent] == 2:
				msgStream = self.EventG(aHost,aComponent,1,self.ComputerEvents)
				self.ComputerStatus[aHost][aComponentId][aComponent] = 1
		elif self.ComputerStatus[aHost][aComponentId][aComponent] == 1:
				msgStream = self.EventG(aHost,aComponent,2,self.ComputerEvents)
				self.ComputerStatus[aHost][aComponentId][aComponent] = 2
		else:
			logging.warning("Error unknown item status")
		return(msgStream)

	def ComputerG(self,aHost):
		msgStream = self.computerEventG(aHost,3,'Power')
		logging.debug("sending : " + msgStream)
		self.sendEvent(self.mySC,msgStream)
		# Clean
		if self.ComputerStatus[aHost][3]['Power'] == 2:
			logging.debug("aHost power recover, will clean all events on it")
			for i in range(0,len(self.ComputerStatus[aHost])):
				for key in self.ComputerStatus[aHost][i]:
					if self.ComputerStatus[aHost][i][key] == 1:
						msgStream = self.computerEventG(aHost,i,key)
						logging.debug("sending : " + msgStream)
						self.sendEvent(self.mySC,msgStream)
						time.sleep(300)
		else:
			numOfComponent = random.randint(0,2)
			logging.debug(str(numOfComponent+1) + " will be affected by power\n")
			i = 0
			while i <= numOfComponent :
				j = random.randint(0,2)
				for key in self.ComputerStatus[aHost][j]:
					if self.ComputerStatus[aHost][j][key] == 2:
						msgStream = self.computerEventG(aHost,j,key)
						logging.debug("sending : " + msgStream)
						self.sendEvent(self.mySC,msgStream)
						time.sleep(300)
						i += 1
		return

	def NetworkG(self,aParentNode) :
		Severity = 5
		alertType =0
		if self.NetworkStatus[aParentNode] == 2:
			alertType = 1
			self.NetworkStatus[aParentNode] = 1
			msgStream = aParentNode + "@@" + self.NetworkEvent['AG'] + "@@" + self.NetworkEvent['AK'] + "@@" + self.NetworkEvent['Summary'] + "@@" + self.NetworkEvent['Manager'] + "@@" + self.NetworkEvent['Agent'] + "@@" + str(Severity) + "@@" + str(alertType) + "ParentRouter" + "\n"
		else :
			alertType = 2
			self.NetworkStatus[aParentNode] = 2
			msgStream = aParentNode + "@@" + self.NetworkEvent['AG'] + "@@" + self.NetworkEvent['AK'] + "@@" + "Link Up" + "@@" + self.NetworkEvent['Manager'] + "@@" + self.NetworkEvent['Agent'] + "@@" + str(Severity) + "@@" + str(alertType) + "ParentRouter" + "\n"
		logging.debug("sending " + msgStream)
		self.sendEvent(self.mySC,msgStream)
		time.sleep(300)
		for subNodeIndex,subNode in self.NetworkR[aParentNode].items():
			if re.match(r'.*2',subNode):
				Severity = 4
			else:
				Severity =3
			msgStream = subNode + "@@" + self.NetworkEvent['AG'] + "@@" + self.NetworkEvent['AK'] + "@@" + self.NetworkEvent['Summary'] + "@@" + self.NetworkEvent['Manager'] + "@@" + self.NetworkEvent['Agent'] + "@@" + str(Severity) + "@@" + str(alertType) + "ChildRouter" + "\n"
			logging.debug("sending " + msgStream)
			self.sendEvent(self.mySC,msgStream)
			time.sleep(60)
		return

	def RGenerator(self):
		logging.info("Now Starting genreate Related event for " + self.number + " times\n")
		numOfIterator = 2 * int(self.number)
		###for i in range(0, numOfIterator):
		iterator = 0
		while iterator < numOfIterator:
			EtypeIndex = random.randint(0,2)
			eType = self.EventType[EtypeIndex]
			#eType = 'Application'
			if eType == 'Network':
				parentNodeIndex = random.randint(0,2)
				parentNode = self.NetworkAllNode[parentNodeIndex]
				self.NetworkG(parentNode)
			elif eType == 'Computer':
				ComputerNodeIndex = random.randint(0,3)
				ComputerNode = self.ComputerAllNode[ComputerNodeIndex]
				self.ComputerG(ComputerNode)
			elif eType == 'Application':
				AppNodeIndex = random.randint(0,3)
				AppNode = self.ApplicationAllNode[AppNodeIndex]
				self.AppG(AppNode)
			else:
				logging.error("Unknow event type to be generated!\n")
				sys.exit(2)
			sleepTime = random.randint(1000,1800) 
			time.sleep(sleepTime)
			iterator += 1
		# final clean
		logging.info("do final clean")
		for PN,status in self.NetworkStatus.items() :
			if status == 1:
				self.NetworkG(PN)
		for aHost in self.ComputerAllNode :
			for i in range(0,len(self.ComputerStatus[aHost])):
				for key in self.ComputerStatus[aHost][i]:
					if self.ComputerStatus[aHost][i][key] == 1:
						msgStream = self.computerEventG(aHost,i,key)
						logging.debug("sending final clean : " + msgStream)
						self.sendEvent(self.mySC,msgStream)
		for aNode in self.ApplicationAllNode :
			if self.ApplicationNodeStatus[aNode] == 1:
				self.AppG(aNode)
		
		self.mySC.close()
		return



	
def RE(n):
	aRE = REvents()
	aRE.number = n
	logging.debug(aRE.aMsg)
	aRE.RGenerator()
	return

def SE(e):
	aSE = SEvent()
	aSE.aEvent = e
	logging.debug(aSE.aMsg)
	aSE.SEventG()
	return

def N(n,m):
	aN = NEvent()
	aN.number = n
	aN.Var = m
	logging.debug(aN.aMsg)
	aN.initEvents(m)
	aN.NEventG()
	return

def main():
	parser = argparse.ArgumentParser(prog=__file__,description='NOI simulator program')
	THelpLine = ['R : genereate related event;', 'S : genereate seasonal event;', 'N : genereae normal random event']
	#parser.add_argument('-t','--type',choices=['R','S','N'],required=True,dest='typeName',help='\n'.join(THelpLine))
	parser.add_argument('-t','--type',choices=['R','S','N'],dest='typeName',help='\n'.join(THelpLine))
	parser.add_argument('-n','--number',nargs='?',default=0,help=' numbers of event (group) to be genereated',dest='number')
	parser.add_argument('-m','--mulplex',nargs='?',default=0,help=' numbers of event per node to be prepared',dest='mulplex')
	parser.add_argument('-e','--event',nargs='?',choices=['A','B','C','D','E'],help='Event to be genereate for Seasonal',dest='event')
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	myInput = parser.parse_args()

	if myInput.typeName == 'R' and not myInput.number:
		print "error : number is requried for R type\n"
		parser.print_help()
		sys.exit(1)
	if myInput.typeName == 'N' and not myInput.mulplex:
		print "error : mulplex is requried for R type\n"
		parser.print_help()
		sys.exit(1)
	if myInput.typeName == 'N' and not myInput.number:
		print "error : number is requried for N type\n"
		parser.print_help()
		sys.exit(1)
	if myInput.typeName == 'S' and not myInput.event:
		print "error : event ID is requried for S type\n"
		parser.print_help()
		sys.exit(1)

	logFile = os.path.dirname(os.path.abspath(__file__)) + '/' +os.path.basename(__file__) + ".log"
	if not os.path.exists(logFile):
		os.system("touch " + logFile)
	logSize = os.path.getsize(logFile)
	if logSize > 1024*1024*20:
		os.system("mv " + logFile + " " + logFile + "_old")
		os.system("> " + logFile)
	logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(levelname)s] [%(process)d] %(message)s',filename = logFile)

	type = myInput.typeName
	number = myInput.number
	event = myInput.event
	mulplex = myInput.mulplex


	if type == 'R':
		logging.info("will genreate " + type + " for " + number + " times") 
		RE(number)
	elif type == 'S':
		logging.info("will genreate " + type)
		SE(event)
	elif type == 'N':
		logging.info("will genreate " + type + " for " + number + " times") 
		N(number,mulplex)
	else :
		logging.info("option input for t is " + type + " which is not supported!\n")
		exit()

	#print("Create new socket...\n")
	#print("Generating Related event...\n")
	#print("Generate random event...\n")
	
if __name__ == '__main__':
    main()




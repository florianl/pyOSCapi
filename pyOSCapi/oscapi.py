# Copyright 2015 Florian Lehner. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import requests
import simplejson as json
import time

_options=(	"captureMode", "captureModeSupport",
			"exposureProgram", "exposureProgramSupport",
			"iso", "isoSupport",
			"shutterSpeed", "shutterSpeedSupport",
			"aperture", "apertureSupport",
			"whiteBalance", "whiteBalanceSupport",
			"exposureCompensation", "exposureCompensationSupport",
			"fileFormat", "fileFormatSupport",
			"exposureDelay", "exposureDelay",
			"sleepDelay", "sleepDelaySupport",
			"offDelay", "offDelaySupport",
			"totalSpace", "remainingSpace",
			"gpsInfo", "dateTimeZone",
			"hdr", "hdrSupport",
			"exposureBracket", "exposureBracketSupport",
			"gyro", "gyroSupport",
			"imageStabilization", "imageStabilizationSupport",
			"wifiPassword"
		)

class OSCAPI:

	def __init__(self, ip, port):
		"""
		:param ip:		IP of the device you want to connect to
		:param port:	Port you want to connect to
		"""
		self.ip		= ip
		self.port	= port
		self.sid	= None
		self.header	= {	"User-Agent":"pyOSCapi",
						"X-XSRF-Protected":"1"}
		self.sess	= requests.session()
		self.options 	= {}
		self.cmds		= []

	def connect(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.startSession"})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		self.sid = (rep["results"]["sessionId"])
		return rep

	def update(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.updateSession", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		return rep

	def disconnect(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.closeSession", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		return rep

	def _checkProgress(self):
		time.sleep(1)
		rep = self.state()
		# this is a workaround which works only for bublcams
		# 
		# the osc api does not define how to integrate the
		# inProgress status in the /osc/state
		if "_bublCommands" in rep["state"]:
			cmdStatus = rep["state"]["_bublCommands"]
			for tmp in cmdStatus:
				if tmp["state"] == "inProgress":
					rep = self._checkProgress()
		return rep

	def takePicture(self, wait=True):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.takePicture", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		if wait == True:
			if rep["state"] == "inProgress":
				rep = self._checkProgress()
		return rep

	def listImages(self, count, size, thumbs):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.listImages", "parameters":{"entryCount":count, "maxSize":size, "includeThumb":bool(thumbs)}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		return rep

	def deleteImage(self, fileUri=None):
		if fileUri == None:
			return
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.delete", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		return rep

	def getImage(self, fileUri=None):
		if fileUri == None:
			return
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.getImage", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		return req

	def getImageMetadata(self, fileUri=None):
		if fileUri == None:
			return
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.getMetadata", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		return rep

	def getOptions(self, optionlist=_options):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.getOptions", "parameters":{"sessionId":self.sid, "optionNames":optionlist}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		for key in rep:
			if key == "results":
				for option in rep[key]["options"]:
					if option in _options:
						self.options[option] = rep[key]["options"][option]
		return rep

	def setOption(self, settings=None):
		if settings == None:
			return
		if not self.options:
			self.getOptions()
		for opt in settings:
			if not self.options.has_key(opt):
				return
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.setOptions", "parameters":{"sessionId":self.sid, "options":settings}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		return rep

	def info(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/info"
		req = requests.get(url, headers=self.header)
		rep = req.json()
		for key in rep:
			if key == "api":
				self.cmds += (rep[key])
		return rep

	def state(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/state"
		req = requests.post(url, headers=self.header)
		rep = req.json()
		return rep

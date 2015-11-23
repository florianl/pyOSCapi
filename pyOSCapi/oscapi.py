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
		print rep
		self.sid = (rep["results"]["sessionId"])
		return

	def update(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.updateSession", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def disconnect(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.closeSession", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def takePicture(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.takePicture", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def listPictures(self, count, size, thumbs):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.listImages", "parameters":{"entryCount":count, "maxSize":size, "includeThumb":bool(thumbs)}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def deletePicture(self, fileUri):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.delete", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def getPicture(self, fileUri):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.delete", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		print req
		return

	def getPictureMetadata(self, fileUri):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.delete", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

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
		return

	def info(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/info"
		req = requests.get(url, headers=self.header)
		rep = req.json()
		print rep
		for key in rep:
			if key == "api":
				self.cmds.append(rep[key])
		return

	def state(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/state"
		req = requests.post(url, headers=self.header)
		rep = req.json()
		print rep
		return

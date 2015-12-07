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

def __execute_request__(kind=None, url=None, headers=None, payload=None):
	if kind == "post":
		try:
			response = requests.post(url, data=payload, headers=headers)
		except requests.exceptions.RequestException as e:
			print "RequestException"
			return None
		except requests.exceptions.ConnectionError as e:
			print "ConnectionError"
			return None
		except requests.exceptions.TooManyRedirects as e:
			print "TooManyRedirects"
			return None
		except requests.exceptions.ConnectTimeout as e:
			print "ConnectTimeout"
			return None
		except requests.exceptions.ReadTimeout as e:
			print "ReadTimeout"
			return None
		except requests.exceptions.Timeout as e:
			print "Timeout"
			return None
	elif kind == "get":
		try:
			response = requests.get(url, data=payload, headers=headers)
		except requests.exceptions.RequestException as e:
			print "RequestException"
			return None
		except requests.exceptions.ConnectionError as e:
			print "ConnectionError"
			return None
		except requests.exceptions.TooManyRedirects as e:
			print "TooManyRedirects"
			return None
		except requests.exceptions.ConnectTimeout as e:
			print "ConnectTimeout"
			return None
		except requests.exceptions.ReadTimeout as e:
			print "ReadTimeout"
			return None
		except requests.exceptions.Timeout as e:
			print "Timeout"
			return None
	else:
		print "Unknown type of http-request"
		return None
	return response

# currently supported options from the OSC API
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
		A device supporting the OSC-API

		:param ip:		IP of the device you want to connect to
		:param port:	Port you want to connect to
		"""
		self.ip		= ip
		self.port	= port
		self.sid	= None
		self.header	= {	"User-Agent":"pyOSCapi",
						"X-XSRF-Protected":"1"}
		self.options 	= {}
		self.cmds		= []

	def connect(self):
		"""
		Opens a connection
		"""
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.startSession"})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
		rep = req.json()
		if rep["state"] == "done":
			self.sid = (rep["results"]["sessionId"])
		return rep

	def update(self):
		"""
		Updates the session
		"""
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.updateSession", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
		rep = req.json()
		return rep

	def disconnect(self):
		"""
		Close the connection
		"""
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.closeSession", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		self.header["Connection"] = "close"
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
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
		"""
		Take a picture via the API

		:param wait:		If True, method will return after taking the picture is done.
							Else you will have to wait by youself.
		"""
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.takePicture", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
		rep = req.json()
		if wait == True:
			if rep["state"] == "inProgress":
				rep = self._checkProgress()
		return rep

	def listImages(self, count, size, thumbs):
		"""
		List the content which is stored on the device

		:param count:		Desired number of entries
		:param size:		maximum size of the returned thumbnail
		:param thumbs:		If True, you will get thumbnails in return.
		"""
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.listImages", "parameters":{"entryCount":count, "maxSize":size, "includeThumb":bool(thumbs)}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
		rep = req.json()
		return rep

	def deleteImage(self, fileUri=None):
		"""
		Delete image on the device

		:param fileUri:		URI of the image
		"""
		if fileUri == None:
			return
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.delete", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
		rep = req.json()
		return rep

	def getImage(self, fileUri=None):
		"""
		Get image from the device

		:param fileUri:		URI of the image
		"""
		if fileUri == None:
			return
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.getImage", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
		return req

	def getImageMetadata(self, fileUri=None):
		"""
		Get the metadata to a image from the device

		:param fileUri:		URI of the image
		"""
		if fileUri == None:
			return
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.getMetadata", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
		rep = req.json()
		return rep

	def getOptions(self, optionlist=_options):
		"""
		Check which options the device supports

		:param optionlist:		specified option you want to check
		"""
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.getOptions", "parameters":{"sessionId":self.sid, "optionNames":optionlist}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
		rep = req.json()
		for key in rep:
			if key == "results":
				for option in rep[key]["options"]:
					if option in _options:
						self.options[option] = rep[key]["options"][option]
		return rep

	def setOption(self, settings=None):
		"""
		Change settings of the device

		:param settings:		Option and Parameter you want to set
		"""
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
		req = __execute_request__("post", url, self.header, data)
		if req == None:
			return None
		rep = req.json()
		return rep

	def info(self):
		"""
		Returns basic information about the device and functionality it supports
		"""
		url = "http://" + self.ip + ":" + self.port +"/osc/info"
		req = __execute_request__("get", url, self.header)
		if req == None:
			return None
		rep = req.json()
		for key in rep:
			if key == "api":
				self.cmds += (rep[key])
		return rep

	def state(self):
		"""
		Returns the state attribute of the device
		"""
		url = "http://" + self.ip + ":" + self.port +"/osc/state"
		req = __execute_request__("post", url, self.header)
		if req == None:
			return None
		rep = req.json()
		return rep

	def getCmds(self):
		"""
		Returns the list of commands the device supports
		"""
		if not self.cmds:
			self.info()
		return self.cmds

	def getSid(self):
		"""
		Returns the current session id
		"""
		return self.sid

	def execCustomCmd(self, cmd=None, payload=None, contentType=None):
		"""
		Execute your own command

		:param cmd:				Command for the request
		:param payload:			Additional data for the command
		:param contentType:		Additional headeri information
		"""
		if cmd == None:
			return
		url = "http://" + self.ip + ":" + self.port + cmd
		req = __execute_request__("post", url, contentType, payload)
		if req == None:
			return None
		rep = req.json()
		return rep

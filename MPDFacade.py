#!/usr/bin/env python

import mpd2 as mpd

class MPDFacade :
	def __init__(self, send_message_function=None, host='localhost', port=6600):
		self.__host = host
		self.__port = port
		self.__client = mpd.MPDClient()
		self.__client.timeout = 10

	def connect(self):
		# TODO : exception handling
		self.__client.connect(self.__host, self.__port)


	####################################
	# Getters

	def currentSong(self) :
		return self.__client.currentsong()

	def status(self) :
		return self.__client.status()


	####################################
	# Playback commands

	def play(self):
		self.__client.play()

	def pause(self):
		self.__client.pause()

	def stop(self):
		self.__client.stop()

	def next(self):
		self.__client.next()

	def prev(self):
		self.__client.previous()

	def volumeUp(self):
		st = self.__client.status()
		curVolume = int(st['volume'])
		curVolume += 10
		if ( curVolume > 100 ) :
			curVolume = 100
		song = self.__client.setvol(curVolume)

	def volumeDown(self):
		st = self.__client.status()
		curVolume = int(st['volume'])
		curVolume -= 10
		if ( curVolume < 0 ) :
			curVolume = 0
		song = self.__client.setvol(curVolume)

	def setPos(self, pos) :
		st = self.__client.status()
		id = st['song']
		p = 0
		if 'time' in st :
			length = int(st['time'].split(':')[1])
			p = pos * length / 100
		self.__client.seek(id, p)


	####################################
	# Outputs

	def outputs(self) :
		res = self.__client.outputs()
		return res

	def enableOutput(self, index, enable) :
		if enable :
			self.__client.enableoutput(index)
		else:
			self.__client.disableoutput(index)


	####################################
	# Playlist

	def playlist(self) :
		list = self.__client.playlistid()
		return list

	def playSong(self, id) :
		self.__client.playid(id)



#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
It's quite a surprise to me that you're currently reading this.

Initially I created this for my own home MPD-based entertainment system, and
yes, I'm aware of existance of many other similar projects. Yes, this is a
perfect example of NIH syndrome (http://lmgtfy.com/?q=nih+syndrome), but I made
my own web MPD client "with blackjack and whores".

I did it because I could and wanted to, and it seemed like a good excercise
since I've never done any web development before other than simple plain HTML.
Having said that, I totally understand that many things might be done
unefficiently, not very elegant, not in Python- or JS-way, of just simply wrong.
If it bothers you you may (moreover: you're strongly encouraged to) contact me
with some details, but it's much better if you send me a pull-request with brief
explanation to the change.

"""

import sys
import os.path
import threading
import json
import cherrypy as Ch

import MPDFacade
import config

'''
Some decorators for further convenience.
'''
# Decorator for REST methods restrictions
def http_methods_allowed(methods=['GET']):
	method = Ch.request.method.upper()
	if method not in methods:
		Ch.response.headers['Allow'] = ", ".join(methods)
		raise Ch.HTTPError(405)
Ch.tools.allow = Ch.Tool('on_start_resource', http_methods_allowed)

# Decorator for not implemented functions
def not_implemented(func):
	def new_f(*args, **kwargs):
		print "----- Not implemented: {0}, params: '{1}'".format(func.__name__, kwargs)
		return json.dumps( { 'error' : "Command '"+func.__name__+"' is not implemented yet" } )
	return new_f


"""
Main CherryPy server class.
"""
class WebMPC(object):

	def __init__(self) :
		self.__mpd_lock = threading.Lock()


	'''
	Web UI main page
	'''
	@Ch.expose
	@Ch.tools.allow(methods=['GET'])
	def index(self):
		f = open('webmpc.html')
		html = f.read()
		f.close();
		return html
	


	####################################
	# Getters

	@Ch.expose
	@Ch.tools.allow(methods=['GET'])
	def currentSong(self) :
		with self.__mpd_lock :
			return json.dumps( mpdFacade.currentSong() )

	@Ch.expose
	@Ch.tools.allow(methods=['GET'])
	def status(self) :
		st = None
		outputs = None
		st_subset = {}

		# status
		with self.__mpd_lock :
			st = mpdFacade.status()
		for key in ['volume', 'time', 'state', 'song', 'songid', 'playlist', 'random'] :
			st_subset[key] = st[key]
		
		# outputs
		with self.__mpd_lock :
			outputs = mpdFacade.outputs()
		st_subset['outputs'] = outputs

		return json.dumps( st_subset )



	####################################
	# Commands

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def volumeUp(self) :
		with self.__mpd_lock :
			mpdFacade.volumeUp()
			return json.dumps( mpdFacade.status() )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def volumeDown(self) :
		with self.__mpd_lock :
			mpdFacade.volumeDown()
			return json.dumps( mpdFacade.status() )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def next(self) :
		with self.__mpd_lock :
			mpdFacade.next()
			return json.dumps( mpdFacade.currentSong() )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def prev(self) :
		with self.__mpd_lock :
			mpdFacade.prev()
			return json.dumps( mpdFacade.currentSong() )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def play(self) :
		with self.__mpd_lock :
			mpdFacade.play()
			return json.dumps( mpdFacade.status() )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def pause(self) :
		with self.__mpd_lock :
			mpdFacade.pause()
			return json.dumps( mpdFacade.status() )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def stop(self) :
		with self.__mpd_lock :
			mpdFacade.stop()
			return json.dumps( mpdFacade.status() )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def setPos(self, pos) :
		with self.__mpd_lock :
			mpdFacade.setPos(int(pos))
			return json.dumps( mpdFacade.status() )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def random(self, on) :
		with self.__mpd_lock :
			mpdFacade.random(on)
			return json.dumps( mpdFacade.status() )


	####################################
	# Outputs

	@Ch.expose
	@Ch.tools.allow(methods=['GET'])
	def outputs(self) :
		with self.__mpd_lock :
			return json.dumps( mpdFacade.outputs() )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def enableOutput(self, index) :
		with self.__mpd_lock :
			mpdFacade.enableOutput(index, True)
			return json.dumps( { 'outputs' : mpdFacade.outputs() } )

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def disableOutput(self, index) :
		with self.__mpd_lock :
			mpdFacade.enableOutput(index, False)
			return json.dumps( { 'outputs' : mpdFacade.outputs() } )


	####################################
	# Playlist

	@Ch.expose
	@Ch.tools.allow(methods=['GET'])
	def playlist(self) :
		with self.__mpd_lock :
			return json.dumps({ 'playlist' : mpdFacade.playlist() })

	@Ch.expose
	@Ch.tools.allow(methods=['POST'])
	def playSong(self, id) :
		with self.__mpd_lock :
			mpdFacade.playSong(id)
			return json.dumps( mpdFacade.currentSong() )


mpdFacade = MPDFacade.MPDFacade(host=config.mpd_host, port=config.mpd_port)
mpdFacade.connect()

if __name__ == '__main__':
	currentDir = os.path.dirname(os.path.abspath(__file__))
	Ch.engine.signal_handler.handlers["SIGINT"] = sys.exit
	Ch.quickstart( WebMPC(), '/', config = {
		'global' : {
			'server.socket_host': config.host,
			'server.socket_port': config.port
			},
		'/js': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(currentDir, 'js')
		},
		'/img': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(currentDir, 'img')
		},
		'/css': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(currentDir, 'css')
		}
	})

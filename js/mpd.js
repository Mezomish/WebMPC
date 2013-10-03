
var MPD = {

	url_base : "",

	setHost : function(host, port) {
		url_base = 'http://' + host + ":" + port;
	},


	// Volume

	volumeUp : function() {
		$.post( url_base + '/volumeUp', null, Callback.onVolume );
	},

	volumeDown : function() {
		$.post( url_base + '/volumeDown', null, Callback.onVolume );
	},


	// Playback

	status : function() {
		$.get( url_base + '/status', null, Callback.onStatus );
	},

	currentSong : function() {
		$.get( url_base + '/currentSong', null, Callback.onCurrentSong );
	},

	play : function() {
		$.post( url_base + '/play', null, Callback.onStatus );
	},

	stop : function() {
		$.post( url_base + '/stop', null, Callback.onStatus );
	},

	pause : function() {
		$.post( url_base + '/pause', null, Callback.onStatus );
	},

	next : function() {
		$.post( url_base + '/next', null, Callback.onCurrentSong );
	},

	prev : function() {
		$.post( url_base + '/prev', null, Callback.onCurrentSong );
	},

	setPos : function(pos) {
		$.post( url_base + '/setPos?pos='+pos, null, Callback.onStatus );
	},

	playSong : function(song_id) {
		$.post( url_base + '/playSong?id='+song_id, null, Callback.onCurrentSong );
	},

	random : function(on) {
		$.post( url_base + '/random?on='+on, null, Callback.onStatus );
	},


	// Outputs

	outputs : function() {
		$.get( url_base + '/outputs', null, Callback.onOutputs );
	},

	enableOutput : function(index) {
		$.post( url_base + '/enableOutput?index='+index, null, Callback.onOutputs );
	},

	disableOutput : function(index) {
		$.post( url_base + '/disableOutput?index='+index, null, Callback.onOutputs );
	},


	// Playlist

	playlist : function() {
		$.get( url_base + '/playlist', null, Callback.onPlaylist );
	}

};

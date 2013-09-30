//
// REST callbacks
//

var Callback = {

	onCurrentSong: function(data, status) {
		// log("Song: " + status + ", data: " + data);
		if ( status === "success" ) {
			updateCurrentSong( jQuery.parseJSON(data) );
		}
		else {
			// TODO : 
		}
	},

	onStatus: function(data, status) {
		// log("Status: " + status + ", data: " + data);
		if ( status === "success" ) {
			updateStatus( jQuery.parseJSON(data) );
		}
		else {
			// TODO : 
		}
	},

	onPlaylist: function(data, status) {
		// log("Playlist: " + status + ", data: " + data);
		if ( status === "success" ) {
			updatePlaylist( jQuery.parseJSON(data) );
		}
		else {
			// TODO : 
		}
	},

	onVolume: function(data, status) {
		// log("Vol: " + status + ", data: " + data);
		if ( status === "success" ) {
			updateStatus( jQuery.parseJSON(data) );
		}
		else {
			// TODO : 
		}
	},

	onOutputs: function(data, status) {
		// log("onOutputs: " + status + ", data: " + data);
		if ( status === "success" ) {
			updateOutputs( jQuery.parseJSON(data) );
		}
		else {
			// TODO :
		}
	}
};

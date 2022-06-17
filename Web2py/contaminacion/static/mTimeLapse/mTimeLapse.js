$(function(){

	var tl = {
		'speeds': {
			'Muy_rapido': 200,
			'Rapido': 300,
			'Medio': 600,
			'Lento': 1200,
			'Muy_lento': 3000
		},
		'advancing': false,
		'img':[],
		'currFrame': 0,
		'fadeTime': 800,
		'sitTime': 0,
		'framefront':false,
		'frameback':false,
		'si': 'false'
	};

	var f = $('#mTimeLapse');
	
	if(f){
		// Setup
		tl.img = f.children('img');
		f.before('<div id="frames"><img id="frame_back"/><img id="frame_front"/></div> <div id="controls"><div id="data_stamp"></div> </div></div>');
		//f.before('  <div class="container"> <div id="frames"><img id="frame_back"/><img id="frame_front"/></div></div> </div>')

		var c = $('#controls');
		c.append('<input type="button" value="Pause" id="pausebutton" onclick="toggleAdvance();"/> ');
		for(var s in tl.speeds){ if(tl.speeds.hasOwnProperty(s)){
			c.append('<input type="button" value="' + (s.replace(/_/g, ' ') + '" onclick="setSpeed(\'' + s + '\');"/>'));
		}}

		// Go
		tl.framefront = $('#frame_front');
		tl.frameback = $('#frame_back');
		advance();
	}

	function advanceFrame() {
		// console.log('Advancing, currframe is ' + tl.currFrame);

		tl.frameback.attr('src', getFrameAttribute('src'));
		tl.currFrame = ((tl.currFrame + 1) % tl.img.length);
		tl.framefront.attr('src', getFrameAttribute('src'));
		tl.framefront.css({'opacity': 1.0});
		//tl.framefront.css({'opacity': 0.0});
		//tl.framefront.animate({'opacity': 1.0},{'duration': tl.fadeTime, 'queue':false});
		tl.framefront.animate({'opacity': 0.1},{'duration': tl.fadeTime, 'queue':false});

		$('#data_stamp').html(getFrameAttribute('data-stamp'));
		// console.log('\t\t>done');
	}

	function getFrameAttribute(attr) {
		var s = tl.img[tl.currFrame].getAttribute(attr);

		//logging
		// console.log(tl.img[tl.currFrame]);
		// console.log(`${attr} returns ${s}`);

		return s || '';
	}

	function advance() {
		window.clearInterval(tl.si);
		// console.log('Advancing, si=' + tl.si);
		tl.advancing = true;
		$('#pausebutton').attr('value', 'Pausar');
		tl.si = setInterval(advanceFrame, (tl.fadeTime + tl.sitTime));
	}

	window.setSpeed = function(name) {
		// console.log('setSpeed ' + name);
		tl.fadeTime = tl.speeds[name] || 500;
		advance();
	};

	window.toggleAdvance = function() {
		tl.advancing = !tl.advancing;
		// console.log('ToggleAdvance - advancing = ' + tl.advancing);

		if(tl.advancing) advance();
		else {
			window.clearInterval(tl.si);
			// console.log('clearInterval cancelled for ' + tl.si);
			$('#pausebutton').attr('value', 'Reproducir');
		}
	};
});
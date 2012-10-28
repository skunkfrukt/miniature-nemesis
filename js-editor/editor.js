$(document).ready(function() {
	var durationToDimensions = function() {
		var minutes = parseFloat($('#stageMinutes').val());
		var width = 640 + minutes * 6000
		var height = 360;  // TODO
		$('#stageWidth').val('' + width);
		$('#stageHeight').val('' + height);
	};
	var dimensionsToDuration = function() {
		var width = parseInt($('#stageWidth').val());
		var minutes = (width - 640) / 6000;
		$('#stageMinutes').val('' + minutes);
	};
	var updateRuler = function() {
		$('#ruler').empty();
		var lengthType = $('#stageLengthType option:selected').text();
		var width = parseInt($('#stageWidth').val());
		for (var i = 0; i <= width; i+= 6000) {
			var x = i + 'px';
			var div = $('<div class="rulerCaption" />');
			div.css('left', x)
			if (i === 0) {
				div.text('0');
			} else if (i % 640 === 0) {
				div.text(i/6000 + 'min' + '/' + i + 'px');
			} else {
				div.text(i/6000 + 'min');
			}
			$('#ruler').append(div);
		}
		for (var i = 0; i <= width; i += 640) {
			if (i % 6000 === 0) {
				continue;
			}
			var x = (i) + 'px';
			var div = $('<div class="rulerCaption" />');
			div.css('left', x)
			div.text(i + 'px');
			$('#ruler').append(div);
		}
	};
	var gameCoordsToEditorCoords = function(el) {
		var height = el.height();
		var x = $.data(el, 'x') + 'px';
		var y = (360 - $.data(el, 'y') - height) + 'px';
		el.css({'top': y, 'left': x});
	};
	var editorCoordsToGameCoords = function(el) {
		var height = el.height();
		var x = el.position().left;
		var y = 360 - el.position().top - el.height();
		$.data($(el), 'x', x);
		$.data($(el), 'y', y);
	};
	var mapDataToJSON = function() {
		var mapData = {};
		mapData['stageID'] = $('#stageID').val();
		mapData['width'] = parseInt($('#stageWidth').val());
		mapData['height'] = parseInt($('#stageHeight').val());
		var spawns = [];
		$('#stageFrame').children().each(function(i, el) {
			var pos = $(el).position();
			var spawn = {};
			spawn['x'] = pos.left;
			spawn['y'] = 360 - pos.top - $(el).height();
			spawn['type'] = $(el).text();
			spawns.push(spawn);
		});
		spawns.sort(function(a, b) {return a.x - b.x;});
		mapData['spawns'] = spawns;
		$('#outputArea').text(JSON.stringify(mapData, null, 4));
	};
	$('#stageDuration').hide();
	$('#stageLengthType').change(function(el) {
		var lengthType = $('#stageLengthType option:selected').text();
		if (lengthType === 'Minutes') {
			dimensionsToDuration();
			$('#stageDimensions').hide();
			$('#stageDuration').show();
		} else if (lengthType === 'Pixels') {
			durationToDimensions();
			$('#stageDuration').hide();
			$('#stageDimensions').show();
		}
		updateRuler();
	});
	$('#updateStageLength').click(function(el) {
		var lengthType = $('#stageLengthType option:selected').text();
		if (lengthType === 'Minutes') {
			durationToDimensions();
		} else if (lengthType === 'Pixels') {
			dimensionsToDuration();
		}
		var stageWidth = $('#stageWidth').val();
		$('#stageFrame').css('width', stageWidth + 'px');
		updateRuler();
		mapDataToJSON();
	});
	$('#addHouse').click(function(el) {
		var div = $('<div class="gameObject propHouse" />');
		div.text('House');
		$.data(div, 'x', $(document).scrollLeft());
		$.data(div, 'y', 0)
		$('#stageFrame').append(div);
		gameCoordsToEditorCoords(div);
		div.draggable({stop: function(ev, ui) {editorCoordsToGameCoords(ui.helper)}});
	});
	$('#addRock').click(function(el) {
		var div = $('<div class="gameObject propRock" />');
		div.text('Rock');
		$.data(div, 'x', $(document).scrollLeft());
		$.data(div, 'y', 0)
		$('#stageFrame').append(div);
		gameCoordsToEditorCoords(div);
		div.draggable({
			stop: function(ev, ui) {
				editorCoordsToGameCoords(ui.helper);
			}
		});
	});
	updateRuler();
	mapDataToJSON();
});

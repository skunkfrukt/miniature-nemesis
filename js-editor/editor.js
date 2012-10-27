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
	});
});

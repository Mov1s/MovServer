function expandMovieSlider(sliderNum) {
    if ($('#sliderMovie' + sliderNum).is(':hidden')) {
        $('#sliderMovie' + sliderNum).slideDown('fast', function () { });
    } else {
        $('#sliderMovie' + sliderNum).slideUp('fast', function () { });
    };
};

function expandMovieText(sliderNum) {
    if ($('#sliderMovieText' + sliderNum).is(':hidden')) {
        $('#sliderMovieText' + sliderNum).slideDown('fast', function () { });
    } else {
        $('#sliderMovieText' + sliderNum).slideUp('fast', function () { });
    };
};

function expandTvSlider(sliderNum) {
    if ($('#sliderTv' + sliderNum).is(':hidden')) {
        $('#sliderTv' + sliderNum).slideDown('fast', function () { });
    } else {
        $('#sliderTv' + sliderNum).slideUp('fast', function () { });
    };
};

function expandTvText(sliderNum) {
	if ($('#sliderTvText' + sliderNum).is(':hidden')) {
		$('#sliderTvText' + sliderNum).slideDown('fast', function () { });
	} else {
		$('#sliderTvText' + sliderNum).slideUp('fast', function () { });
	};
};

function movieTab() {
    $('#contentWrapper').attr('style', 'left: 0px');
	$('#container').attr('style', 'background-image: url("blue_gradient.png");');
	$('#menu').attr('style', 'background-color: #00A7E2;');
	$('.header').attr('style', 'border-bottom: 1px solid #00A7E2;');
};
function tvTab() {
    $('#contentWrapper').attr('style', 'left: -100%');
	$('#container').attr('style', 'background-image: url("red_gradient.png");');
	$('#menu').attr('style', 'background-color: #C9000C;');
	$('.header').attr('style', 'border-bottom: 1px solid #C9000C;');
};
function infoTab() {
    $('#contentWrapper').attr('style', 'left: -200%');
	$('#container').attr('style', 'background-image: url("green_gradient.png");');
	$('#menu').attr('style', 'background-color: #52A200;');
	$('.header').attr('style', 'border-bottom: 1px solid #52A200;');
};

function approveMovie(mid, tid) {
    window.location = "index.php?action=approveMovie&mid=" + mid + "&tid=" + tid;
};

function ignoreMovie(mid) {
    window.location = "index.php?action=ignoreMovie&mid=" + mid;
};

function customMovie(mid) {
	expandMovieSlider(mid);
	expandMovieText(mid);
};

function approveTv(eid){
	window.location = "index.php?action=approveTv&eid=" + eid;
};

function ignoreTv(eid){
	window.location = "index.php?action=ignoreTv&eid=" + eid;
};

function customTv(eid){
	expandTvSlider(eid);
	expandTvText(eid);
};

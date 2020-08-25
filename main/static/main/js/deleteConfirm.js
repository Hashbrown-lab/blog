$(document) .ready(function() {
	$(document) .on('click', '.deleteConfirm', function() {
		return confirm("You sure?");
	});
});
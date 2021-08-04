function check_style_status() {
	var solu = document.getElementById("solution").value;
	var answer = document.getElementById("user-answer").value;
	var proceed = document.getElementById("submit_button");
	let text;
	if (solu == answer) {
	  text = 'Nice work!';
	} else {
		text = 'Not quite... the correct answer was:';
    document.getElementById("sol").innerHTML = solu;
	}
	// Lock submit button to prevent submitting twice
  document.getElementById("check_answer").className="disappear";
	document.getElementById("submit_button").className="appear";
	document.getElementById('user-answer').readOnly = true;
// Return result to page
  document.getElementById("feedback").innerHTML = text;
}

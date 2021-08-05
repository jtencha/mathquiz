function check_style_status() {
	var solution = document.getElementById("solution").value;
	var answer = document.getElementById("user-answer").value;
	var proceed = document.getElementById("submit_button");
	let text;
	if (solution == answer) {
		var responses = [ "Nice Work!", "Awesome!", "Excellent!", "Great Job!"];
		var picking = Math.floor(Math.random() * responses.length);
  	var final = responses[picking];
	  text = final;
	} else {
		var responses = ["Almost! ", "Not quite! ", "Oof! ", "*Disappointing Trombone Music* "]
		var picking = Math.floor(Math.random() * responses.length);
		var final = responses[picking];
    text = final + "The correct answer was " + solution + ".";
	}
	// Lock submit button to prevent submitting twice
  document.getElementById("check_answer").className="disappear";
	document.getElementById("submit_button").className="appear";
	document.getElementById('user-answer').readOnly = true;
// Return result to page
  document.getElementById("feedback").innerHTML = text;
}

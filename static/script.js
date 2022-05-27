var onLoad = new Date();
function timer() {
  return (new Date() - onLoad) / 1000;
}

function check() {
	var time = timer();
	var cap = document.getElementById("time_per").value;
	var solution = document.getElementById("solution").value;
	var answer = document.getElementById("user_answer").value;
	var proceed = document.getElementById("submit_button");
	let text;
	if (time > cap) {
		//set the answer as none so the python reads it as incorrect
		document.doquiz.user_answer.value = "";
		text = "You exceeded your " + cap + " second limit!";
	}
	else if (solution == answer) {
		var responses = [ "Nice Work!", "Awesome!", "Excellent!", "Great Job!", "Correct!", "That's Right!"];
		var picking = Math.floor(Math.random() * responses.length);
  	var final = responses[picking];
	  text = final;
	} else {
		var responses = ["Almost! ", "Not quite! ", "Oof! ", "*Disappointing Trombone Music* ", "Incorrect."]
		var picking = Math.floor(Math.random() * responses.length);
		var final = responses[picking];
    text = final + "The correct answer was " + solution + ".";
	}
	// Lock submit button to prevent submitting twice
  document.getElementById("check_answer").className="disappear";
	document.getElementById("submit_button").className="appear";
	document.getElementById('user_answer').readOnly = true;
// Return result to page
  document.getElementById("feedback").innerHTML = text;
}

function stop() {
  if (window.event.keyCode == 13) {
        event.returnValue = false;
        event.cancel = true;
    }
}

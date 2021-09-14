var onLoad = new Date();
function timer() {
  return (new Date() - onLoad) / 1000;
}

function check_style_status() {
	let time = timer();
	let cap = document.getElementById("time_per").value;
	let solution = document.getElementById("solution").value;
	let answer = document.getElementById("user_answer").value;
	let proceed = document.getElementById("submit_button");
	let text;
	if (time > cap) {
		//set the answer as none so the python reads it as incorrect
		document.doquiz.user_answer.value = "";
		text = "You exceeded your " + cap + " second limit!";
	}
	else if (solution == answer) {
		let responses = [ "Nice Work!", "Awesome!", "Excellent!", "Great Job!"];
		let picking = Math.floor(Math.random() * responses.length);
  		let final = responses[picking];
	  	text = final;
	} else {
		let responses = ["Almost! ", "Not quite! ", "Oof! ", "*Disappointing Trombone Music* "]
		let picking = Math.floor(Math.random() * responses.length);
		let final = responses[picking];
    		text = final + "The correct answer was " + solution + ".";
	}
// Lock submit button to prevent submitting twice
document.getElementById("check_answer").className="disappear";
document.getElementById("submit_button").className="appear";
document.getElementById('user_answer').readOnly = true;
// Return result to page
document.getElementById("feedback").innerHTML = text;
}

//Function that animates text to appear that it is being typed
function typer(element, msg, speed) {
  for (let i = 0; i <= msg.length; i++) { //For each charecter in the text
		if (msg.substring(i-4,i+4).includes('&nbsp') == false) {
    	setTimeout(() => {element.innerHTML = msg.substring(0, i)}, speed*i); //Sets a delay for each character based on the speed argument
		}
	}
}
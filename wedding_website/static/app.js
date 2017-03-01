console.log("hello world");
var nav = document.getElementById('nav');

nav.addEventListener('mouseover', function(event) {
	if(event.target.tagName === "A") {
		event.target.style.color = "#B8DDB4";
		event.target === event.target.toUpperCase;
	}
});

nav.addEventListener('mouseout', function(event) {
	if(event.target.tagName === "A") {
		event.target.style.color = "#6b9966";
	}
});

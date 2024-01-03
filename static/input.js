//Variable Declaration

var centre = { //Default centre coordinates
    lat: 51.3572864,
		lng: -2.3560192};
let markers = [];
var map;

//Functions
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, fail);
    } else {
        console.log("Browser Does not Support Geolocation");
    }
}

//Is run in the event that the user accepts location permissions
function success(position) {
    centre = { //Centres the map on the user's location
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };
}

//Is run in the event that the user rejects location permissions
function fail(error) {
    if (error.PERMISSION_DENIED) {
        console.log("The User have denied the request for Geolocation.");
    }
}

function initMap() {
		//Creates the map
    map = new google.maps.Map(document.getElementById('map-input'), {
				//Defines map settings
        center: centre, 
        disableDefaultUI: true,
        gestureHandling: 'greedy',
        zoom: 8, //Starting zoom level
				//Style information
        styles: [{
                "featureType": "all",
                "elementType": "labels.text",
                "stylers": [{
                    "color": "#ffffff"
                }]
            },
            {
                "featureType": "all",
                "elementType": "labels.text.fill",
                "stylers": [{
                        "saturation": 9
                    },
                    {
                        "color": "#ffffff"
                    },
                    {
                        "lightness": 10
                    }
                ]
            },
            {
                "featureType": "all",
                "elementType": "labels.text.stroke",
                "stylers": [{
                        "visibility": "on"
                    },
                    {
                        "color": "#000000"
                    },
                    {
                        "lightness": 5
                    }
                ]
            },
            {
                "featureType": "all",
                "elementType": "labels.icon",
                "stylers": [{
                    "visibility": "off"
                }]
            },
            {
                "featureType": "administrative",
                "elementType": "geometry.fill",
                "stylers": [{
                        "color": "1c2333"
                    },
                    {
                        "lightness": 0
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "geometry.stroke",
                "stylers": [{
                        "color": "#1c2333"
                    },
                    {
                        "lightness": -24
                    },
                    {
                        "weight": 1.2
                    }
                ]
            },
            {
                "featureType": "landscape",
                "elementType": "geometry",
                "stylers": [{
                        "color": "#1c2333"
                    },
                    {
                        "lightness": 0
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "geometry",
                "stylers": [{
                        "color": "#1c2333"
                    },
                    {
                        "lightness": 8
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry.fill",
                "stylers": [{
                        "color": "#1c2333"
                    },
                    {
                        "lightness": -24
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry.stroke",
                "stylers": [{
                        "color": "#1c2333"
                    },
                    {
                        "lightness": 36
                    },
                    {
                        "weight": 0.2
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "geometry",
                "stylers": [{
                        "color": "#1c2333"
                    },
                    {
                        "lightness": -16
                    }
                ]
            },
            {
                "featureType": "road.local",
                "elementType": "geometry",
                "stylers": [{
                        "color": "#1c2333"
                    },
                    {
                        "lightness": -28
                    }
                ]
            },
            {
                "featureType": "transit",
                "elementType": "geometry",
                "stylers": [{
                        "color": "#1c2333"
                    },
                    {
                        "lightness": -8
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry",
                "stylers": [{
                        "color": "#5192c9"
                    },
                    {
                        "lightness": -25
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry.fill",
                "stylers": [{
                        "color": "#5192c9"
                    },
                    {
                        "saturation": -25
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels.icon",
                "stylers": [{
                    "color": "#ff0000"
                }]
            }
        ]
    });

		//Listens for clicks over the map
    map.addListener('click', function(e) {
        placeMarker(e.latLng, map); //If a click is detected this function is called
    });

    function placeMarker(position, map) { //Creates a new node
        var marker = new google.maps.Marker({ //Places marker on map
            position: position,
            map: map,
            icon: {
                url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
            }
        });
        map.panTo(position); //Centres map on the marker's location
        console.log('New marker at ' + position); //Logs the creation of the node
        markers.push(position); //Adds the node's coordinates to an array to be sent to the server on submission
    }
}


//Function that sends array of nodes to the server to be processed
async function postMarkers(method, markers) {
    try {
       let res = await axios({
            url: '/post',
            method: 'post',
            timeout: 8000,
				 		data: {method:method, markers:markers}
        });
				if(res.status == 200){
            console.log("Confirmation of data received")
        }    
    }
    catch (err) { //In the event of an error..
        console.error(err); //it is logged
    }
}

//Selects all elements with id=submit
const lst = document.querySelectorAll('[id=submit]');
for (var i = 0; i<lst.length; i++){ //For each 'submit' element
	lst[i].onclick = function() { //Do this on click
		var method = (this.textContent || this.innerText).trim().slice(2); //Get the method from the elements innerHTML
		//Won't send off data if there aren’t at least two nodes or if the algorithm will take too long
		//Improvement if i had time: add maximum amount of nodes for other algorithms and feedback that there were too many nodes somehow
		if ((markers.length > 1) && !(method == 'bruteforce' &&  markers.length > 9)) { 
			//Uses above function to send nodes to the server
			postMarkers(method, markers);
			window.location.replace("/loading") 
		}
	};
}

//Adds open/close functionality for the dropdown menus
const dropdowns = document.querySelectorAll(".dropdown");
dropdowns.forEach(el => {
  const button = el.querySelector(".dropdown-btn");
  button.addEventListener("click", () => {
    //Only one dropdown can be open at a time
		//All dropdowns are closed
    [...dropdowns].filter(x => x != el).forEach(el => el.classList.remove("is-open"));
		//The specific drowpdown being clicked is opened
		el.classList.toggle("is-open");
  });
});

//Driver Code
getLocation(); //Tries set the map centre as the user's location
window.initMap = initMap; //Initialises the map
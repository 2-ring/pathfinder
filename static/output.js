//Variable Declaration
var centre = path[0]
var map;

//Functions

function initMap() {
		//Creates the map
    map = new google.maps.Map(document.getElementById('map-output'), {
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

	if (typeof path === 'string' || path instanceof String) {
		path = JSON.parse(path);} //JSON to array

	//Defines the path in terms of polylines
	const solution = new google.maps.Polyline({
        path: path,
        geodesic: true,
        strokeColor: "#3779b3", //line color
        strokeOpacity: 1.0,
        strokeWeight: 2, //line thickness
    });
		solution.setMap(map); //Adds the path to the map

	//Places the markers on the map
	for (let i = 0; i < path.length; i++) { //For each node in the path
		new google.maps.Marker({
					position: path[i],
					map,
					icon: { //Specifies the image to be used for the markers
							url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
					}
			});
	}
}

function create_download_link() {
	//Formatting path as an easily readible string
	var path_string = ''
	for (let node of path) { //For each node in the path
		for (let dir of ['lat', 'lng']) { //For each component of the coordinate
			path_string += dir+': '+node[dir]+'\r\n'
	}
		path_string += '\r\n\r\n'} //Adding blank space between nodes

	//Logs the formatted path to console
	console.log('Path recived:\r\n\r\n'+path_string)
	//Logs method to console
	console.log('Using: '+method)

	// Creating the download link HTML element
	var download_link = document.createElement('a'); //Creating new HTML link element
  download_link.setAttribute('href', 'data:text/plain;charset=utf-8,' + path_string); //Adding url
  download_link.setAttribute('download', 'path.txt'); //Defining as a download link
	download_link.setAttribute('class', 'blue'); //Adding class
	const text = document.createTextNode("here"); //Defining text node
	download_link.appendChild(text); //Adding text node to link
	
	const download_popup = document.getElementsByClassName('download_popup')[0];
	//Adds the new element to the download_link div
	download_popup.appendChild(download_link);
}

function show_popup(){
	//Creates a dictionary that converts the phrase received to the name of the corresponding popup
	const method_to_popup = {'bruteforce':'bruteforce', 'a pure genetic algorithm':'genetic', 'a seeded genetic algorithm':'genetic', 'christofides algorithm':'christofides', 'a mst-dfs algorithm':'mst-dfs'};
	setTimeout(() => {window.location.replace("#"+method_to_popup[method]);}, 7000);
}

function slow_popup_transition() {
	for (let info_popup of document.getElementsByClassName("overlay")){ //For each div with class "overlay"
	info_popup.classList.add('slow_transition');} //Add class slow_transition
}


//Driver Code

//Initialises the map
window.initMap = initMap;
//Creates a link to allow for the path to be dowloaded
create_download_link();
//Slows the default popup transition speed
slow_popup_transition();
//Displays an algorithm info popup based on which algorithm was used
show_popup();
//Scrolls to bottom of page so text based results can be seen (after 3secs)
setTimeout(() => {window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth' });}, 3000);
	
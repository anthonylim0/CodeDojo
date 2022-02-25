let markers = [];
let colors = [
  "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/orange-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/ltblue-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/pink-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
  "http://maps.google.com/mapfiles/ms/icons/purple-dot.png",
];
const imagePath =
  "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m";
function finalStun(list, carpark) {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 16,
    center: { lat: carpark[0][0], lng: carpark[0][1] },
  });

  for (let i = 0; i < list.length; i++) {
    const position = new google.maps.LatLng(list[i][0], list[i][1]);
    const marker = new google.maps.Marker({
      position: position,
      icon: colors[list[i][2]],
      fiilOpacity: 0.4,
      strokeWeight: 0.5,
      map: map,
    });
    markers.push(marker);
  }

  const iconBase =
    "https://developers.google.com/maps/documentation/javascript/examples/full/images/";
  const icons = {
    parking: {
      icon: iconBase + "parking_lot_maps.png",
    },
  };

  for (let i = 0; i < carpark.length; i++) {
    const position = new google.maps.LatLng(carpark[i][0], carpark[i][1]);
    const marker = new google.maps.Marker({
      position: position,
      icon: icons["parking"].icon,
      scale: 2,
      map: map,
    });
  }
}

function finalStun2() {
  setMapOnAll(null);
}

function setMapOnAll(map) {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

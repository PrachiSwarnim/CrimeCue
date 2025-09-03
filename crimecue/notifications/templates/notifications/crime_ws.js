const socket = new WebSocket('ws://127.0.0.1:8000/ws/crimes/');

socket.onmessage = function(event) {
    const crime = JSON.parse(event.data);
    console.log("New Crime reported:", crime);

    const crimeList = document.getElementById("crime-list");
    const item = document.createElement("div");

    // Display a readable summary
    item.textContent = `${crime.title} at ${crime.city} - ${crime.published_at}`;
    crimeList.prepend(item); // Add to top
};

socket.onopen = function() {
    console.log("WebSocket connection established");
};

socket.onclose = function() {
    console.log("WebSocket connection closed");
};

socket.onerror = function(error) {
    console.error("WebSocket error:", error);
};

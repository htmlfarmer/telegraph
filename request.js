function GET(file, callback) {
  var http = new XMLHttpRequest();
  http.onload = callback;
  http.open("GET", file);
  http.send();
}

function POST(file, data, callback) {
  var http = new XMLHttpRequest();
  http.onload = callback;
  http.open("POST", file);
  http.send(data);
}

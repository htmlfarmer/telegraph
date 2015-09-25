// SQLHttpRequest Post Request
function pyhttp (file, callback) {

  var http = new XMLHttpRequest();
  http.onload = callback;
  http.open("GET", file);
  http.send();
  //var post = "";
  //http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  //http.setRequestHeader("Content-length", post.length);
  //http.setRequestHeader("Connection", "close");
  //http.send(post);
}

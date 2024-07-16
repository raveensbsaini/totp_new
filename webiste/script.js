console.log("this is random text");

function get_cookie(name){
  let vari = document.cookie;
  let a = vari.split(';')
  for (var i = 0 ; i < a.length; i++ ){
    console.log(i);
    let string = a[i];
    let string1 = string.split("=");
    if (string1[0] == name) {
      return string1[1];
    };
  };
  return ""

};

console.log(document.cookie.length);
if (document.cookie.length === 0){
  console.log("there is no cookie");
  window.location.href = "./login/index.html";
}
else {
  let session_cookie = get_cookie("session_cookie");
  if (session_cookie == ""){
    console.log("cookie exits but not exact one");
    window.location.href = "./login/index.html";
  }
  else {
    console.log(`this is your cookie ${session_cookie} waiting for show you some code`);

  };
};
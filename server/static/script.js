
function display(parent,list){
  let element = document.querySelector(`#${parent}`);
  let array = [];
  for (let t = 0;t<list.length;t++){
    array.push(document.querySelector(`#${list[t]}`))
  };
  let children = element.children;
  for (let i = 0;i < children.length;i++){
    if (array.includes(children[i]) ){
      children[i].style.display = "block";
    }
    else {
      children[i].style.display = "none";
    }
  };
};


async function main(cookie) {
  let url = "/cookie" 
  let data = {"cookie":cookie};
  let object = {"method":"POST",
                "headers":{"Content-Type":"application/json"},
              "body":JSON.stringify(data) };
              
              
  let res = await fetch(url,object);
  if (res.status != 200){
    window.location.href = "/web/login/index.html";
  };
  let body = await res.json();
  let key = body["key"];
  let password_hash = body["password"];
  let username = body["username"];
  window.key = key;
  if ( typeof(window.password) == "undefined"){
    display("result",["enter_password"]);
    document.querySelector("#click_password").onclick = () => {
      document.querySelector("#enter_password_message").innerHTML = "";
      let check = document.querySelector("#enter_password_text").value;
      let p = check;
      check = CryptoJS.SHA256(check).toString();
      if (check == password_hash){
        window.password = p;
        display("result",["add_key","if_key"]);
        document.querySelector("#welcome").innerHTML = `welcome ${username}`;
        if (key == "None"){
          console.log("this function works key == ");
          document.querySelector("#none_key").innerHTML = "no app present please add some";
        }
        else {};
        document.querySelector("#add_app").onclick = () =>{
          console.log("user want to add app");
          console.log(window.key);
          if (key == "None"){
            let a  = {};
            let a_key = document.querySelector("#name_of_app").value;
            let a_value = document.querySelector("#secret_key").value;
            a[a_key] = a_value;
            console.log(a,typeof(a));
            a = JSON.stringify(a);
            console.log(a,typeof(a));
            console.log(window.password);
            var encrypt = CryptoJS.AES.encrypt(a,window.password);
            console.log(encrypt,typeof(encrypt));
          };
        };
      }
      else{
        document.querySelector("#enter_password_message").innerHTML = "wrong password please try again";
      };
    };
  };
};
function get_cookie(name){
  let vari = document.cookie;
  let a = vari.split(';')
  for (var i = 0 ; i < a.length; i++ ){
    let string = a[i];
    let string1 = string.split("=");
    if (string1[0] == name) {
      return string1[1];
    };
  };
  return ""

};
if (document.cookie.length === 0){
  console.log("there is no cookie");
  window.location.href = "/web/login/index.html";
  localStorage.setItem("reason",'empty cookie');
}
else {
  let session_cookie = get_cookie("session_cookie");
  if (session_cookie == ""){
    console.log("cookie exits but no cookie named session_cookie");
    localStorage.setItem("reason","cookie exits but no session cookie");
    window.location.href = "./login/index.html";
  }
  else {
    main(session_cookie);
    console.log(`this is your cookie ${session_cookie} waiting for show you some code`);
    localStorage.setItem("reason","cookie exits name session");

  };
};
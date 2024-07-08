
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

async function set_data(username,password,key){
  let url = "/set_data/" + encodeURIComponent(username);

  password = CryptoJS.SHA256(password).toString();
  let data = {"key":key,
              "password":password
              };
  window.data = data;
  let object = {
                "method":"POST",
                "headers":{"Content-Type":"application/json"},
                "body":JSON.stringify(data)
                
                };
  let res = await fetch(url,object)
  if(res.status != 200){
    document.querySelector("#add_key_messaage").innerHTML = "cannot add app some error";
    
  }
  else{
    window.location.href = "/index.html";
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
    window.location.href = "/login/index.html";
  };
  let body = await res.json();
  let key = body["key"];
  let password_hash = body["password"];
  let username = body["username"];
  window.username = username;
  window.key = key;
  if ( typeof(window.password) == "undefined"){
    display("result",["enter_password"]);
    document.querySelector("#click_password").onclick = () => {
      document.querySelector("#enter_password_message").innerHTML = "";
      let check = document.querySelector("#enter_password_text").value;
      let  p = document.querySelector("#enter_password_text").value;
      check = CryptoJS.SHA256(check).toString();
      if (check == password_hash){
        window.password = p;
        display("result",["add_key","if_key"]);
        document.querySelector("#welcome").innerHTML = `welcome ${username}`;
        if (key == "None"){
          document.querySelector("#none_key").innerHTML = "no app present please add some";
        }
        else {
          let decrypted_data = CryptoJS.AES.decrypt(window.key,window.password);
          decrypted_data = decrypted_data.toString(CryptoJS.enc.Utf8);
          
          decrypted_data = JSON.parse(decrypted_data);
          window.decrypted_data  = decrypted_data;

          let parent = document.querySelector("#ordered_list")
          for ( let i in decrypted_data) {
            const element = document.createElement("li");
            let token = window.otplib.authenticator.generate(decrypted_data[i]);
            element.innerHTML = `${i} : ${token}`;
            parent.appendChild(element);
          };

        };
        document.querySelector("#add_app").onclick = () =>{
          let a;
          if (key == "None"){
             a  = {};
          }
          else {
             a = window.decrypted_data;
          };

            let a_key = document.querySelector("#name_of_app").value;
            let a_value = document.querySelector("#secret_key").value;
            try  {
                let random = window.otplib.authenticator.generate(a_value);
                a[a_key] = a_value;
                a = JSON.stringify(a);
                var encrypt = CryptoJS.AES.encrypt(a,window.password);
                window.encrypt = encrypt.toString();
                localStorage.setItem("encrypted",window.encrypt);
                set_data(username,window.password,window.encrypt);
            }
            catch {
              document.querySelector("#add_key_message").innerHTML = "this secrket key is not valid check it again";
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
  window.location.href = "/login/index.html";
}
else {
  let session_cookie = get_cookie("session_cookie");
  if (session_cookie == ""){
    window.location.href = "/login/index.html"
  }
  else {
    main(session_cookie);

  };
};
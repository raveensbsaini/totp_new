console.log("this is signup");
async function main(username,password,recovery_key){
  username = encodeURIComponent(username);
  password  = CryptoJS.SHA256(password).toString();
  recovery_key = CryptoJS.SHA256(recovery_key).toString();
  let url = "/signup/" + username;
  let data = {"password":password,
              "recovery_key":recovery_key
              };
  let object = { method:"POST",
                headers:{"Content-Type": "application/json"},
                body:JSON.stringify(data)
                }; 
  let res = await fetch(url,object);
  if (res.status == 200){
    window.location.href = "/web/index.html";
  }
  else {
   let element_error = document.querySelector("#error");
   element_error.innerHTML = "either username or password is incorrect. Please try again!"  
  };

};
document.addEventListener("DOMContentLoaded",()=>{
  let element = document.querySelector("#login");
  element.onclick = function (){
    window.location.href = '../login/index.html';
  };
  let element_signup = document.querySelector("#signup");
  element_signup.onclick = function () {
    let username = document.querySelector("#username").value;
    let password = document.querySelector("#password").value;
    let recovery_key = document.querySelector("#recover_key").value;
    main(username,password,recovery_key);
  };
});
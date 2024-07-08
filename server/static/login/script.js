async function main(url,data){
  let res = await fetch(url,{
    method:"POST",
    body:data,
    headers: { // Optional headers (e.g., Content-Type)
    'Content-Type': 'application/json' // Specify JSON content
  }
  });
  if (res.status == 200){
    window.location.href = "/index.html"
  }
  else{
    document.querySelector("#error").innerHTML = "either username or password is not correct. Please try again."
  };
};

document.addEventListener('DOMContentLoaded',()=>{
  let element = document.querySelector("#signup");
  element.onclick = function (){
    window.location.href = "../signup/index.html";
    
  };
  let element_login = document.querySelector("#login");
  element_login.onclick = function () {
    let username = document.querySelector("#username").value;
    username = encodeURIComponent(username);
    let password = document.querySelector("#password").value;
    password = CryptoJS.SHA256(password).toString();
    let data = {"password":password}
    data = JSON.stringify(data);
    let url = "/get_data/";
    url = url + username;
    main(url,data);
    
  };
});

// data = {}


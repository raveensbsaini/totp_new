console.log("this is a test")

async function main(url,data){
  fetch(url,{
    method:"POST",
    body:data,
    headers: { // Optional headers (e.g., Content-Type)
    'Content-Type': 'application/json' // Specify JSON content
  }
  }).then(response => response.json()).then(data => {console.log(data);});
};

document.addEventListener('DOMContentLoaded',()=>{
  let element = document.querySelector("#signup");
  console.log(element);
  element.onclick = function (){
    window.location.href = "../signup/index.html";
    
  };
  console.log("this is line no 10");
  let element_login = document.querySelector("#login");
  console.log(element_login);
  console.log("this is line no 13");
  element_login.onclick = function () {
    console.log("login button clicked");
    let username = document.querySelector("#username").value;
    username = encodeURIComponent(username);    const password = document.querySelector("#password").value;
    let data = {"password":password}
    data = JSON.stringify(data);
    let url = "http://0.0.0.0:8000/get_data/";
    url = url + username;
    console.log(url);
    main(url,data);
    
  };
});

// data = {}


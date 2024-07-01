console.log("this is signup");
document.addEventListener("DOMContentLoaded",()=>{
  let element = document.querySelector("#login");
  console.log(element);
  element.onclick = function (){
    window.location.href = '../login/index.html';
  };
});
console.log("this is a test")
document.addEventListener('DOMContentLoaded',()=>{
  let element = document.querySelector("#signup");
  console.log(element);
  element.onclick = function (){
    window.location.href = "../signup/index.html";
  };
});
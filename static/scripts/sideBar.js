var open = false

function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}

function toggleNav() {
  if(open) {
    closeNav()
  }
  else {
    openNav()
  }

  open = !open
}
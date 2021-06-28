export function openNav() {
    document.getElementById("mySidebar").style.width = "180px";
    document.getElementById("main").style.marginLeft = "180px";
    document.getElementById("openbtn").style.display = "none";
    document.getElementById("closebtn").style.display = "inline";
}

export function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
    document.getElementById("openbtn").style.display = "inline";
    document.getElementById("closebtn").style.display = "none";
}
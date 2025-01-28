

function changeVisibility(element) {

    if (typeof element === "string") {
        element = document.getElementById(element);
    }
    if (element) {
        element.hidden = !(element.hidden);
    } else {
        console.log("IN changeVisibility: element not found");
    }
}


function changeVisibilityClass(clName) {

    let els = document.getElementsByClassName(clName);
    for (let i = 0; i < els.length; i++) {
        changeVisibility(els[i]);
    }

}
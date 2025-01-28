
function getVariables() {

    console.log("in sending");

    let targetEl = document.getElementById("variables-place");

    let formElement = document.getElementById('search-form');
    let url = formElement.dataset.url;

    console.log(url);

    let formValues = htmx.values(formElement);
    console.log(formValues);

    let prom = htmx.ajax('POST', url, {target : targetEl, swap : 'innerHTML', source : formElement, values: formValues});
    prom.then(function () {
        console.log("after promise");
    })

}

function getPlot() {
    console.log("in getting plot");

    let formElement = document.getElementById('vars-form');
    let url = formElement.dataset.url;

    console.log(url);

    let formValues = htmx.values(formElement);
    console.log(formValues);

    let prom = htmx.ajax('POST', url, {source : formElement, values: formValues});
    prom.then(function () {
        console.log("after promise");
    })
    
}
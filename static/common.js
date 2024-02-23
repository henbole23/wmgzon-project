// Converts prices to correct decimal place
function priceConversion(tag, className) {
    let divs = document.querySelectorAll(`${tag}.${className}`);
    console.log(divs)
    // Loop through each price
    divs.forEach(function (divElement) {
        let currentValue = parseFloat(divElement.innerHTML);
        console.log(currentValue)
        if (!isNaN(currentValue)) {
            // Round to two decimal places
            let roundedValue = currentValue.toFixed(2);
            divElement.innerHTML = '£' + roundedValue;
        }
    });

}

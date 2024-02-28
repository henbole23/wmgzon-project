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

// Highlights the current category selected
function categoryIdentifier() {
    const currentPath = window.location.pathname;
    console.log('POO')
    console.log(currentPath)
    const id = currentPath.replace("/category/", "")

    const currentPage = document.getElementById(id);
    currentPage.classList.add("active")
}

// Sorts products by year in ascending or descending order
function sortProductYear() {
    console.log('sortProducts Ran');
    const sortDirection = document.getElementById('sortOptions').value;
    const productsContainer = document.getElementById('products');
    let products = Array.from(productsContainer.querySelectorAll('.product'));
    console.log(products)
    products.sort(function (a, b) {
        const aValue = parseInt(a.getAttribute('data-year'));
        console.log(aValue)
        const bValue = parseInt(b.getAttribute('data-year'));
        console.log(bValue)
        return sortDirection === 'descend' ? bValue - aValue : aValue - bValue;
    });

    products.forEach(function (product) {
        productsContainer.appendChild(product);
    });
}

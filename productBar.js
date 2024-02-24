const template = document.createElement('template');

number = 1

template.innerHTML = `
    <div class="productCard">
        <p>{ number }</p>
    </div>
`;


document.body.appendChild(template.content)

function displayProducts(products) {
    const container = document.getElementById('productBar');

    products.foreach(product => {
        const card = document.createElement('div');
        card.classList.add('productCard');

        card.innerHTML = `
            <p>HI</p>   
        `;
        container.appendChild(card)
        
    })
} 
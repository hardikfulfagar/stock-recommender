document.getElementById('fetchButton').addEventListener('click', async () => {
    try {
        const response = await fetch('http://localhost:5000/fetch_stock_data', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        alert('Failed to fetch stock data. Please try again later.');
    }
});

function displayResults(data) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = ''; // Clear any previous results
    if (data.length === 0) {
        resultDiv.textContent = 'No recommendations available.';
        return;
    }

    data.forEach(stock => {
        const div = document.createElement('div');
        div.className = `recommendation ${stock.recommendation.toLowerCase()} border`;
        const h3 = document.createElement('h3');
        h3.textContent = `${stock.company} (${stock.symbol})`;
        const p1 = document.createElement('p');
        p1.textContent = `Recommendation: ${stock.recommendation}`;
        const p2 = document.createElement('p');
        p2.textContent = `RSI: ${stock.RSI.toFixed(2)}`;
        const p3 = document.createElement('p');
        p3.textContent = `Price: $${stock.price.toFixed(2)}`;
        div.appendChild(h3);
        div.appendChild(p1);
        div.appendChild(p2);
        div.appendChild(p3);
        resultDiv.appendChild(div);
    });
}

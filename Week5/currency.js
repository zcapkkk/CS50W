document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').onsubmit = function() {
        //console.log("Submission received");
    fetch('https://api.exchangeratesapi.io/latest?base=USD')
    .then(response => response.json())
    .then(data => {
        const currency = document.querySelector('#currency').value.toUpperCase();
        
        const rate = data.rates[currency];

        if (rate !== undefined) {
            document.querySelector('div').innerHTML =  `1 USD is equal to ${rate.toFixed(3)} ${currency}`;

        }
        else {
            document.querySelector('div').innerHTML = "Invalid Currency";

        }





    })


    .catch(error => {
        console.log('Error: ', error);
    });

    return false;
}
});
var pages = document.getElementById("previous_requests");


document.addEventListener("DOMContentLoaded", () => {
    fetch("/previous_requests",
    {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then( request => {
        request.json().then(function(data) {
            let contactrequest = data['contactrequest'];

            for (let ownerId in contactrequest){
                pages.innerHTML += `
                    <div class="previous_requests_obj">
                    <p>` + contactrequest[ownerId]['createdAt'] + `</p>
                    <p>` + contactrequest[ownerId]['reqtext'] + `</p>
                    <br>
                    </div>
                `;
            }
        });
    })
    .catch( error => {
        alert(error);
        console.error('error:', error);
    });

});
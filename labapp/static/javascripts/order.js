var sendbtn = document.getElementById("sendbtn");

//order



sendbtn.addEventListener("click", function (e) {
    e.preventDefault();
    let fname = document.getElementsByName("fname")[0].value;
    let lname = document.getElementsByName("lname")[0].value;
    let email = document.getElementsByName("email")[0].value;
    let number = document.getElementsByName("number")[0].value;
    let num_of_ad = document.getElementsByName("user_profile_color_1")[0].value;
    let num_of_child = document.getElementsByName("user_profile_color_2")[0].value;
    let reqtext = document.getElementsByName("reqtext")[0].value;

    if (!(fname && lname && email && number && num_of_ad && num_of_child)) {
        alert("Пожалуйста, заполните все поля для отправки ");
    }
    else {
        var formdata = JSON.stringify({ fname: fname, lname: lname, email: email, number: number, num_of_ad: num_of_ad, num_of_child: num_of_child, reqtext: reqtext});
       console.log(formdata);
        fetch("/order",
        {
            method: "POST",
            body: formdata,
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then( response => {
            response.json().then(function(data) {
                console.log(data)
            });
        })
        .catch( error => {
            alert(error);
            console.error('error:', error);
        });
    }

});
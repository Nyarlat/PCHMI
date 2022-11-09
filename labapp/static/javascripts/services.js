function func_show(obj) {
  document.getElementById(obj).classList.toggle("show");
}

function click_atag(obj1,obj2) {
  str = document.getElementById(obj1);
  search = document.getElementById(obj2);
  search.value = str.text;
  prnt = str.parentElement
  prnt.classList.toggle("show");
}

function search_d() {
    var name,place,date;
    var result;
    place = document.getElementById("myInput1").value;
    type_of_place = document.getElementById("myInput2").value;
    var formdata = JSON.stringify({place: place, type: type_of_place});
    fetch("/api/tour",
    {
       method: "POST",
       body:formdata,
       headers: {
            'Content-Type': 'application/json'
        }
    }).then( response => {
        response.json().then(function(data) {
            result = data;
            input_data = document.getElementById("myInput3");
            input_data.value = result;
            input_data.min = result;
            input_data.max = result;
        });
    })
}

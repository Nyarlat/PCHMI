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

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtЗначение = a[i].textСодержание || a[i].innerText;
    if (txtЗначение.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function searchd(){
    let input1, input2;
    input1 = document.getElementById("myInput1").value;
    input2 = document.getElementById("myInput2").value;
    let formdata = JSON.stringify({ place: input1, typeoftour: input2});
    console.log(formdata)

    fetch("api/tour",
    {
        method: "POST",
        body: formdata,
        headers: {
            'Content-Type': 'application/json'
        }
    })
   .then( response => {
        // fetch в случае успешной отправки возвращает Promise, содержащий response объект (ответ на запрос)
        // Возвращаем json-объект из response и получаем данные из поля message
        response.json().then(function(data) {
            console.log(data)
            alert(data.message);
        });
    })
    .catch( error => {
        alert(error);
        console.error('error:', error);
    });
    }

//var sendbtn = document.getElementsByClassName("dropbtn")   // выбираем DOM-елемент (кнопку)

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
            alert(result);
        });
    })
    date = document.getElementById("myInput3").value;
}

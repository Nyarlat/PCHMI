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
            let statfield = document.getElementById("myInput3");
            statfield.value = result;
        });
    })
    date = document.getElementById("myInput3").value;
}

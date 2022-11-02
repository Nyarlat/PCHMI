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

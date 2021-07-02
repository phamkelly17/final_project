document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#dropdown').addEventListener('click', () => open_dropdown());
    document.addEventListener('click', close_dropdown);

    load_page();
})

function load_page(){
    var select_quantity = document.getElementsByClassName('select-quantity')
    
    for(var j = 0; j < select_quantity.length; j++) {
        //select_quantity[j].id = `select-quantity${j}`;
        for (var i = 1; i <= 10; i++){
            var option = document.createElement("option")
            option.innerHTML = i;
            option.value = i;
            select_quantity[j].appendChild(option);
        }
    }
    
}

function add_cart (name) {

    var item = name;
    select_quantity = document.getElementsByClassName(item)[0];
    quantity = select_quantity.selectedOptions[0].value;

    fetch ('addCart', {
        method: "POST",
        body: JSON.stringify ({
            "item":item,
            "quantity":quantity
        })
    })
    select_quantity.selectedIndex = 0;
    var message = document.querySelector('#menu-message-view');
    message.style.display = 'block';
    message.innerHTML = "Added to cart"
    close_message();
    location.reload();
    return false;
}

function delete_cart (name) {
    fetch('deleteCart', {
        method: "PUT",
        body: JSON.stringify({
            item: name
        })
    });
    location.reload();
}
 
function place_order () {
    fetch ('placeOrder', {
        method: "PUT",
        body: JSON.stringify ({
            read: true,
        })
    });
    location.reload();
    return false;
}

function close_message(){
    setTimeout(function(){ 
        var message = document.querySelector('#menu-message-view');
        message.style.display = "none";
    }, 3000);
}

function open_dropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function close_dropdown(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

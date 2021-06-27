document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#dropdown').addEventListener('click', () => open_dropdown());
    document.addEventListener('click', close_dropdown);

})

function order_completed (id) {
    console.log("here");
    fetch ('completeOrder', {
        method: "PUT",
        body: JSON.stringify ({
            completed: true,
            id: id,
        })
    });
    location.reload()
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
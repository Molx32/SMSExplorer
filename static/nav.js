function open_modal(modal_id){
	m = document.getElementById(modal_id);
	m.style.display = "block";
	window.onclick = function(event){
		if(event.target == m){
			m.style.display = "none";
		}
	}

	span = document.getElementsByClassName("close")[0];
	span.onclick = function(){
		m.style.display = "none";
	}
}


function displayData(button_id){
    m = document.getElementById("data_viewer");
    // Local vars
	id = button_id.split('_').pop().replace('"','');
	url = "/api/get_data?id=" + id;

    // Build request
	var update_form = new XMLHttpRequest();
	update_form.open('GET', url, true);
	update_form.setRequestHeader('Content-Type', 'application/json');
    update_form.onload = function() {console.log(update_form.responseText)};
	update_form.onreadystatechange = () => {
        if (update_form.readyState === 4) {
            obj = JSON.parse(JSON.parse(update_form.response));
            var node = new PrettyJSON.view.Node({
                el:document.getElementById("result"),
                data:obj
            });
          open_modal('data_viewer');
        }
      };

	// Send request
	update_form.send();
}
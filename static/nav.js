
// Update menu display
// current_menu_id = 'menu_' + window.location.pathname.replace('/','')
// element = document.getElementById(current_menu_id);
// element.classList.add('active')


//
var coll = document.getElementsByClassName("collapsible");
console.log(coll);
var i;

for (i = 0; i < coll.length; i++) {
	coll[i].addEventListener("click", function() {
	// this.classList.toggle("active");
	var content = this.nextElementSibling;
	if (content.style.maxHeight){
		content.style.maxHeight = null;
	} else {
		content.style.maxHeight = content.scrollHeight + "px";
	} 
	});
}




/* **************************************** */
/*               SEARCH FORMS               */
/* **************************************** */
set_form('include');
set_form('exclude');
search_bar = document.getElementById('input_search');
search_bar.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    send_search_form();
  }
});

function findGetParameter(parameterName) {
    var result = null, tmp = [];
    location.search.substr(1).split("&").forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}

function send_search_form() {
	form = document.getElementById('form_search');
	param_search 	= document.getElementById('input_search').value;
	param_include 	= document.getElementById('include_selector').innerText;
	param_exclude 	= document.getElementById('exclude_selector').innerText;

	// Normalize param_include
	if (param_include === "None") {
		param_include = "NONE"
	} else if (param_include === "URLs") {
		param_include = "URL"
	} else if (param_include === "Data") {
		param_include = "DATA"
	}

	// Normalize param_exclude
	if (param_exclude === "None") {
		param_exclude = "NONE"
	} else if (param_exclude === "URLs") {
		param_exclude = "URL"
	} else if (param_exclude === "Data") {
		param_exclude = "DATA"
	}

	document.getElementById('form_input_search').value	= param_search;
	document.getElementById('form_input_include').value = param_include;
	document.getElementById('form_input_exclude').value = param_exclude;
	form.submit();
}

function set_form(filter_type){
	// Set search input
	document.getElementById("input_search").value = findGetParameter('search');
	
	// Set filters
	filter 			= findGetParameter('input_' + filter_type);
	var none 		= document.getElementById("toggle_" + filter_type + "_none");
	var valid_urls 	= document.getElementById("toggle_" + filter_type + "_valid_urls");
	var valid_data 	= document.getElementById("toggle_" + filter_type + "_valid_data");
	var selector 	= document.getElementById(filter_type + '_selector')
	if(filter === "NONE"){
		selector.style.left = 0;
		selector.style.width = none.clientWidth + "px";
		selector.style.backgroundColor = "#5CB8A6";
		selector.innerHTML = "None";
	}else if(filter === "URL"){
		selector.style.left = none.clientWidth + "px";
		selector.style.width = valid_urls.clientWidth + "px";
		selector.innerHTML = "URLs";
		selector.style.backgroundColor = "#5CB8A6";
	}else if(filter === "DATA"){
		selector.style.left = none.clientWidth + valid_urls.clientWidth + 1 + "px";
		selector.style.width = valid_data.clientWidth + "px";
		selector.innerHTML = "Data";
		selector.style.backgroundColor = "#5CB8A6";
	}
}

function change_filter(filter, type){
	// Handle new settings
	var none 		= document.getElementById("toggle_" + type + "_none");
	var valid_urls 	= document.getElementById("toggle_" + type + "_valid_urls");
	var valid_data 	= document.getElementById("toggle_" + type + "_valid_data");
	var selector 	= document.getElementById(type + "_selector");
	if(filter === "none"){
		selector.style.left = 0;
		selector.style.width = none.clientWidth + "px";
		selector.style.backgroundColor = "#5CB8A6";
		selector.innerHTML = "None";
	}else if(filter === "valid_urls"){
		selector.style.left = none.clientWidth + "px";
		selector.style.width = valid_urls.clientWidth + "px";
		selector.innerHTML = "URLs";
		selector.style.backgroundColor = "#5CB8A6";
	}else if(filter === "valid_data"){
		selector.style.left = none.clientWidth + valid_urls.clientWidth + 1 + "px";
		selector.style.width = valid_data.clientWidth + "px";
		selector.innerHTML = "Data";
		selector.style.backgroundColor = "#5CB8A6";
	}
	send_search_form()
}






/* **************************************** */
/*               DATA DISPLAY               */
/* **************************************** */
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

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
if (location.pathname.includes('search')) {
	set_form();
}

function findGetParameter(parameterName) {
    var result = null, tmp = [];
    location.search.substr(1).split("&").forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}

function set_search_form() {
	form = document.getElementById('form_search');
	param_search 		= document.getElementById('input_search').value;
	param_include 		= document.getElementById('data_selector').innerText;
	param_interesting 	= document.getElementById('interesting_selector').innerText;
	
	document.getElementById('form_input_search').value	= param_search;
	document.getElementById('form_input_data').value = param_include;
	document.getElementById('form_input_interesting').value = param_interesting;
}

function send_search_form() {
	param_search = document.getElementById('input_search').value;
	document.getElementById('form_input_search').value	= param_search;
	form.submit();
}

function set_form(){
	// Set search input
	document.getElementById("input_search").value = findGetParameter('search');
	data_filter 		= findGetParameter('input_data').toUpperCase();
	interesting_filter 	= findGetParameter('input_interesting').toUpperCase();

	change_filter_data(data_filter);
	change_filter_interesting(interesting_filter);
}

function change_filter_data(filter){
	// Handle new settings
	var none 	= document.getElementById("toggle_data_none");
	var yes 	= document.getElementById("toggle_data_yes");
	var no 		= document.getElementById("toggle_data_no");
	var selector = document.getElementById("data_selector");
	if(filter.toUpperCase() === "NONE"){
		selector.style.left = 0;
		selector.style.width = none.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "NONE";
	}else if(filter.toUpperCase() === "YES"){
		selector.style.left = none.clientWidth + "px";
		selector.style.width = yes.clientWidth + "px";
		selector.innerHTML = "YES";
		selector.style.backgroundColor = "#2daab8";
	}else if(filter.toUpperCase() === "NO"){
		selector.style.left = none.clientWidth + yes.clientWidth + 1 + "px";
		selector.style.width = no.clientWidth + "px";
		selector.innerHTML = "NO";
		selector.style.backgroundColor = "#2daab8";
	}
	set_search_form()
}

function change_filter_interesting(filter){
	// Handle new settings
	var all 		= document.getElementById("toggle_interesting_all");
	var none 		= document.getElementById("toggle_interesting_none");
	var yes 		= document.getElementById("toggle_interesting_yes");
	var no 			= document.getElementById("toggle_interesting_no");
	var selector 	= document.getElementById("interesting_selector");
	if(filter.toUpperCase() === "ALL"){
		selector.style.left = 0;
		selector.style.width = all.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "ALL";
	}else if(filter.toUpperCase() === "YES"){
		selector.style.left = all.clientWidth + "px";
		selector.style.width = yes.clientWidth + "px";
		selector.innerHTML = "YES";
		selector.style.backgroundColor = "#2daab8";
	}else if(filter.toUpperCase() === "NO"){
		selector.style.left = all.clientWidth + yes.clientWidth + 1 + "px";
		selector.style.width = no.clientWidth + "px";
		selector.innerHTML = "NO";
		selector.style.backgroundColor = "#2daab8";
	}else if(filter.toUpperCase() === "NONE"){
		selector.style.left = all.clientWidth + yes.clientWidth + no.clientWidth + 1 + "px";
		selector.style.width = none.clientWidth + "px";
		selector.innerHTML = "NONE";
		selector.style.backgroundColor = "#2daab8";
	}
	set_search_form()
}


function send_search_form_targets() {
	form = document.getElementById('form_search');
	param_search 	= document.getElementById('input_search_targets').value;

	// NOrmalize param_include
	document.getElementById('form_input_search_targets').value = param_search;
	form.submit();
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



/* *************************************** */
/*               EXPORT DATA               */
/* *************************************** */
function export_smss() {
	const req = new XMLHttpRequest();
	req.open("GET", "/settings/export_smss");
	req.send();
}
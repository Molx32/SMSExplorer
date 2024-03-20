/* **************************************************** */
/*               BUTTON VALUES MANAGEMENT               */
/* **************************************************** */
// The goal of this sections is to update all buttons with
// the appropriate date loading a page

// SEARCH PAGES
if (location.pathname.includes('search')) {
	smsSearchDisplaySearchBar();
}
// INVESTIGATION PAGES
if (location.pathname.includes('investigation')) {
	investigationDisplaySearchBar();
}

// Read get parameters to set button in an appropriate way
function findGetParameter(parameterName) {
    var result = "", tmp = [];
    location.search.substr(1).split("&").forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}




/* ************************************** */
/*               SMS SEARCH               */
/* ************************************** */
function smsSearchDisplaySearchBar(){
	// Get params
	search 		= findGetParameter('search');
	data 		= findGetParameter('data');
	interesting = findGetParameter('interesting');
	// Update visuals
	document.getElementById("smssearch_search_button").value = search
	smsSearchDisplayToggleButtonData(data)
	smsSearchDisplayToggleButtonInteresting(interesting);
}

function smsSearchDisplayToggleButtonInteresting(filter){
	// Handle new settings
	var all 		= document.getElementById("smssearch_toggle_interesting_all");
	var none 		= document.getElementById("smssearch_toggle_interesting_none");
	var yes 		= document.getElementById("smssearch_toggle_interesting_yes");
	var no 			= document.getElementById("smssearch_toggle_interesting_no");
	var selector 	= document.getElementById("smssearch_toggle_interesting_selector");
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
}

function smsSearchDisplayToggleButtonData(filter){
	// Handle new settings
	var none 	= document.getElementById("smssearch_toggle_data_none");
	var yes 	= document.getElementById("smssearch_toggle_data_yes");
	var no 		= document.getElementById("smssearch_toggle_data_no");
	var selector = document.getElementById("smssearch_toggle_data_selector");
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
}

function smsSearchSendSearchForm() {
	// Retrieve values from buttons
	param_search 		= document.getElementById('smssearch_search_button').value;
	param_include 		= document.getElementById('smssearch_toggle_data_selector').innerText;
	param_interesting 	= document.getElementById('smssearch_toggle_interesting_selector').innerText;
	// Update form
	document.getElementById('smssearch_form_search').value		= param_search;
	document.getElementById('smssearch_form_data').value 		= param_include;
	document.getElementById('smssearch_form_interesting').value = param_interesting;
	// Send form
	form = document.getElementById('sms_search_form');
	form.submit();
}

/* ****************************************** */
/*               INVESTIGATION               */
/* ***************************************** */
function investigationDisplaySearchBar(){
	// Set search input
	search = findGetParameter('search');
	unique = findGetParameter('unique');
	
	document.getElementById("investigation_search_button").value = search
	investigationDisplayToggleButton(unique);
}

function investigationDisplayToggleButton(unique){
	// Visual update of the toggle button
	var yes 		= document.getElementById("investigation_toggle_unique_yes");
	var no 			= document.getElementById("investigation_toggle_unique_no");
	var selector 	= document.getElementById("investigation_toggle_unique_selector");
	if(unique.toUpperCase() === "NO"){
		selector.style.left = 0;
		selector.style.width = no.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "NO";
	}else if(unique.toUpperCase() === "YES"){
		selector.style.left = no.clientWidth + "px";
		selector.style.width = yes.clientWidth + "px";
		selector.innerHTML = "YES";
		selector.style.backgroundColor = "#2daab8";
	}
}

function investigationDisplayUnqualifiedButton(unqualified){
	// Visual update of the toggle button
	var yes 		= document.getElementById("investigation_toggle_unqualified_yes");
	var no 			= document.getElementById("investigation_toggle_unqualified_no");
	var selector 	= document.getElementById("investigation_toggle_unqualified_selector");
	if(unqualified.toUpperCase() === "NO"){
		selector.style.left = 0;
		selector.style.width = no.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "NO";
	}else if(unqualified.toUpperCase() === "YES"){
		selector.style.left = no.clientWidth + "px";
		selector.style.width = yes.clientWidth + "px";
		selector.innerHTML = "YES";
		selector.style.backgroundColor = "#2daab8";
	}
}

function investigationSendSearchForm() {
	// Retrieve values from buttons
	search	= document.getElementById('investigation_search_button').value;
	unique	= document.getElementById('investigation_toggle_unique_selector').innerText;
	unqualified	= document.getElementById('investigation_toggle_unqualified_selector').innerText;
	// Update form
	document.getElementById('investigation_form_search').value = search;
	document.getElementById('investigation_form_toggle_unique').value = unique;
	document.getElementById('investigation_form_toggle_unqualified').value = unqualified;
	// Send form
	form = document.getElementById('investigation_search_form');
	form.submit();
}

function investigationUpdateDisplayToggleButton(domain, value){
	// Handle new settings
	var yess 		= document.getElementsByName(domain + "_no");
	var nos 			= document.getElementsByName(domain + "_yes");
	var selectors 	= document.getElementsByName(domain + "_selector");

	for (let i = 0; i < yess.length; i++) {
		selector 	= selectors[i]
		yes 		= yess[i]
		no 			= nos[i]
		if(value.toUpperCase() === "NO"){
			selector.style.left = 0;
			selector.style.width = no.clientWidth + "px";
			selector.style.backgroundColor = "#2daab8";
			selector.innerHTML = "NO";
			document.getElementsByName(domain + "_not_interesting_buttons")[0].hidden = false;
    		document.getElementsByName(domain + "_interesting_buttons")[0].hidden = true;
		}else if(value.toUpperCase() === "YES"){
			selector.style.left = no.clientWidth + "px";
			selector.style.width = yes.clientWidth + "px";
			selector.innerHTML = "YES";
			selector.style.backgroundColor = "#2daab8";
			document.getElementsByName(domain + "_not_interesting_buttons")[0].hidden = true;
    		document.getElementsByName(domain + "_interesting_buttons")[0].hidden = false;
		}
	  }
}

function investigationUpdateDisplayTagsButton(domain, tag){
	// Handle new settings
	e 	= document.getElementsByName(domain + "_" + tag)[0]

	// 
	if (e.classList.contains("tag-active")) {
		e.classList.remove("tag-active");
	} else {
		e.classList.add("tag-active")
	}
}

function investigationUpdateSendInterestingForm(domain) {
	// Retrieve is_interesting
	var is_interesting 	= document.getElementsByName(domain + "_selector")[0].innerHTML;
	// Retrieve not interesting tags
	div_not_interesting_button = document.getElementsByName(domain + '_not_interesting_buttons')[0]
	is_not_interesting_tags = div_not_interesting_button.getElementsByClassName('tag-active')
	div_interesting_button = document.getElementsByName(domain + '_interesting_buttons')[0]
	is_interesting_tags = div_interesting_button.getElementsByClassName('tag-active')
	
	// 
	tags_list = []
	if (is_interesting === 'YES') {
		for (tag of is_interesting_tags) {
			tags_list.push(tag.innerHTML)
		}
		tags = tags_list.join()
	} else if (is_interesting === 'NO') {
		for (tag of is_not_interesting_tags) {
			tags_list.push(tag.innerHTML)
		}
		tags = tags_list.join()
	} else {
		tags = ''
	}
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			// Typical action to be performed when the document is ready:
			alert("Updated");
		}
	};
	xhttp.open("POST", "/investigation/target/interesting?domain=" + domain + "&is_interesting=" + is_interesting + "&tags=" + tags, true);
	xhttp.send();
}

function investigationUpdateSendTagForm() {
	
}



function set_search_form_investigation_is_interesting() {
	// Send a request
	param_search 		= document.getElementById('input_search').value;
	param_interesting 	= document.getElementById('investigation_toggle_unique_selector').innerText;
	
	document.getElementById('form_input_search').value	= param_search;
	document.getElementById('form_input_unique').value = param_interesting;
}



/* *********************************** */
/*               TARGETS               */
/* *********************************** */
function targetsSendSearchForm() {
	form = document.getElementById('form_search');
	param_search 	= document.getElementById('input_search_targets').value;

	// Normalize param_include
	document.getElementById('form_input_search').value = param_search;
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



/* ************************************ */
/*               SETTINGS               */
/* ************************************ */
function export_smss() {
	const req = new XMLHttpRequest();
	req.open("GET", "/settings/export_smss");
	req.send();
}

function settings_clean_database() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			// Typical action to be performed when the document is ready:
			alert("Database cleaned");
		}
	};
	xhttp.open("GET", "/settings/database/clean", true);
	xhttp.send();
}

function settings_update_targets() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			// Typical action to be performed when the document is ready:
			alert("Database cleaned");
		}
	};
	xhttp.open("GET", "/settings/database/targets_update", true);
	xhttp.send();
}
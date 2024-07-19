/* **************************************************** */
/*               BUTTON VALUES MANAGEMENT               */
/* **************************************************** */
// The goal of this sections is to update all buttons with
// the appropriate date loading a page

// SEARCH PAGES
if (location.pathname.includes('search')) {
	smsSearchDisplaySearchBar();
}
// CATEGORIZE PAGES
if (location.pathname.includes('categorize')) {
	categorizeDisplaySearchBar();
}
// AUTOMATION PAGE
if (location.pathname.includes('automation')) {
	automationSearchDisplaySearchBar();
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
	smsSearchDisplayToggleButtonInteresting(interesting);
	smsSearchDisplayToggleButtonData(data)
}

function smsSearchDisplayToggleButtonInteresting(filter){
	// Handle new settings
	var all 		= document.getElementById("smssearch_toggle_interesting_all");
	var none 		= document.getElementById("smssearch_toggle_interesting_none");
	var yes 		= document.getElementById("smssearch_toggle_interesting_yes");
	var no 			= document.getElementById("smssearch_toggle_interesting_no");
	var selector 	= document.getElementById("smssearch_toggle_interesting_selector");
	if(filter.toUpperCase() === "ALL" || filter.toUpperCase() === ""){
		selector.style.left = 0;
		selector.style.width = all.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "🚫";
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
	if(filter.toUpperCase() === "NONE"  || filter.toUpperCase() === ""){
		selector.style.left = 0;
		selector.style.width = none.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "🚫";
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

	if (param_include == '🚫'){
		param_include = 'NONE'
	}

	if (param_interesting == '🚫'){
		param_interesting = 'ALL'
	}

	// Update form
	document.getElementById('smssearch_form_search').value		= param_search;
	document.getElementById('smssearch_form_data').value 		= param_include;
	document.getElementById('smssearch_form_interesting').value = param_interesting;
	// Send form
	form = document.getElementById('sms_search_form');
	form.submit();
}

function auditLogsSearchSendSearchForm() {
	// Retrieve values from buttons
	param_search 		= document.getElementById('auditlogs_search_button').value;

	// Update form
	document.getElementById('audit_logs_search_form_search').value		= param_search;

	// Send form
	form = document.getElementById('audit_logs_search_form');
	form.submit();
}


/* ***************************************** */
/*               categorize               */
/* ***************************************** */
function categorizeDisplaySearchBar(){
	// Set search input
	search = findGetParameter('search');
	unqualified = findGetParameter('unqualified');
	
	document.getElementById("categorize_search_button").value = search
	categorizeDisplayUnqualifiedButton(unqualified);
}

function categorizeDisplayUnqualifiedButton(unqualified){
	// Visual update of the toggle button
	var yes 		= document.getElementById("categorize_toggle_unqualified_yes");
	var no 			= document.getElementById("categorize_toggle_unqualified_no");
	var selector 	= document.getElementById("categorize_toggle_unqualified_selector");
	if(unqualified.toUpperCase() === "NO"  || unqualified.toUpperCase() === ""){
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

function categorizeSendSearchForm() {
	// Retrieve values from buttons
	search	= document.getElementById('categorize_search_button').value;
	unqualified	= document.getElementById('categorize_toggle_unqualified_selector').innerText;
	// Update form
	document.getElementById('categorize_form_search').value = search;
	document.getElementById('categorize_form_toggle_unqualified').value = unqualified;
	// Send form
	form = document.getElementById('categorize_search_form');
	form.submit();
}

function categorizeUpdateDisplayToggleButton(domain, value){
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
			// Switch 'not_interesting' visible and 'interesting' invisible
			elements = document.getElementsByName(domain + "_not_interesting_buttons")
			for (j=0; j < elements.length; j++){elements[j].hidden=false}
			elements = document.getElementsByName(domain + "_interesting_buttons")
			for (j=0; j < elements.length; j++){elements[j].hidden=true}
		}else if(value.toUpperCase() === "YES"){
			selector.style.left = no.clientWidth + "px";
			selector.style.width = yes.clientWidth + "px";
			selector.innerHTML = "YES";
			selector.style.backgroundColor = "#2daab8";
			// Switch 'not_interesting' visible and 'interesting' invisible
			elements = document.getElementsByName(domain + "_not_interesting_buttons")
			for (j=0; j < elements.length; j++){elements[j].hidden=true}
			elements = document.getElementsByName(domain + "_interesting_buttons")
			for (j=0; j < elements.length; j++){elements[j].hidden=false}
		}
	  }
}

function categorizeUpdateDisplayTagsButton(domain, tag){
	// Handle new settings
	elements = document.getElementsByName(domain + "_" + tag)
	for (i=0; i < elements.length; i++){
		e = elements[i];
		if (e.classList.contains("tag-active")) {
			e.classList.remove("tag-active");
		} else {
			e.classList.add("tag-active")
		}
	}
}

function categorizeUpdateSendInterestingForm(domain) {
	// Retrieve is_interesting
	var is_interesting 	= document.getElementsByName(domain + "_selector")[0].innerHTML;
	console.log(is_interesting)
	// Retrieve not interesting tags
	div_not_interesting_button = document.getElementsByName(domain + '_not_interesting_buttons')[0]
	console.log(div_not_interesting_button)
	is_not_interesting_tags = div_not_interesting_button.getElementsByClassName('tag-active')
	console.log(is_not_interesting_tags)
	div_interesting_button = document.getElementsByName(domain + '_interesting_buttons')[0]
	console.log(div_interesting_button)
	is_interesting_tags = div_interesting_button.getElementsByClassName('tag-active')
	console.log(is_interesting_tags)
	
	// 
	tags_list = []
	if (is_interesting === 'YES') {
		for (tag of is_interesting_tags) {
			label = tag.getAttribute('name').replace(domain + '_','')
			tags_list.push(label)
		}
		tags = tags_list.join()
	} else if (is_interesting === 'NO') {
		for (tag of is_not_interesting_tags) {
			label = tag.getAttribute('name').replace(domain + '_','')
			tags_list.push(label)
		}
		tags = tags_list.join()
		console.log(tags)
	} else {
		tags = ''
		console.log(tags)
	}
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			displayNotification("Updated", "Target changed")
		}
	};
	console.log("POST", "/categorize/target/update?domain=" + domain + "&is_interesting=" + is_interesting + "&tags=" + tags)
	xhttp.open("POST", "/categorize/target/update?domain=" + domain + "&is_interesting=" + is_interesting + "&tags=" + tags, true);
	xhttp.send();
}


/* ************************************** */
/*               AUTOMATION               */
/* ************************************** */
function targetsSendSearchForm() {
	form = document.getElementById('form_search');
	param_search 	= document.getElementById('input_search_targets').value;

	// Normalize param_include
	document.getElementById('form_input_search').value = param_search;
	form.submit();
}

function automationSearchDisplaySearchBar(){
	// Get params
	search 		= findGetParameter('search');
	legal 		= findGetParameter('legal');
	automated 	= findGetParameter('automated');
	// Update visuals
	document.getElementById("automation_search_button").value = search
	automationDisplayLegalButton(legal);
	automationDisplayAutomatedButton(automated)
}

function automationDisplayLegalButton(legal){
	// Handle new settings
	var all 		= document.getElementById("automation_toggle_legal_all");
	var yes 		= document.getElementById("automation_toggle_legal_yes");
	var no 			= document.getElementById("automation_toggle_legal_no");
	var selector 	= document.getElementById("automation_toggle_legal_selector");
	if(legal.toUpperCase() === "ALL" || legal.toUpperCase() === ""){
		selector.style.left = 0;
		selector.style.width = all.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "ALL";
	}else if(legal.toUpperCase() === "YES"){
		selector.style.left = all.clientWidth + "px";
		selector.style.width = yes.clientWidth + "px";
		selector.innerHTML = "YES";
		selector.style.backgroundColor = "#2daab8";
	}else if(legal.toUpperCase() === "NO"){
		selector.style.left = all.clientWidth + yes.clientWidth + 1 + "px";
		selector.style.width = no.clientWidth + "px";
		selector.innerHTML = "NO";
		selector.style.backgroundColor = "#2daab8";
	}
}

function automationDisplayAutomatedButton(automated){
	// Handle new settings
	var all 		= document.getElementById("automation_toggle_automated_all");
	var yes 		= document.getElementById("automation_toggle_automated_yes");
	var no 			= document.getElementById("automation_toggle_automated_no");
	var selector 	= document.getElementById("automation_toggle_automated_selector");
	if(automated.toUpperCase() === "ALL" || automated.toUpperCase() === ""){
		selector.style.left = 0;
		selector.style.width = all.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "ALL";
	}else if(automated.toUpperCase() === "YES"){
		selector.style.left = all.clientWidth + "px";
		selector.style.width = yes.clientWidth + "px";
		selector.innerHTML = "YES";
		selector.style.backgroundColor = "#2daab8";
	}else if(automated.toUpperCase() === "NO"){
		selector.style.left = all.clientWidth + yes.clientWidth + 1 + "px";
		selector.style.width = no.clientWidth + "px";
		selector.innerHTML = "NO";
		selector.style.backgroundColor = "#2daab8";
	}
}

function automationUpdateDisplayLegalButton(domain, value){
	// Handle new settings
	var no 			= document.getElementsByName(domain + "_legal_no")[0];
	var yes 		= document.getElementsByName(domain + "_legal_yes")[0];
	var selector 	= document.getElementsByName(domain + "_legal_selector")[0];

	if(value.toUpperCase() === "NO"){
		selector.style.left = 0;
		selector.style.width = no.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "NO";
	}else if(value.toUpperCase() === "YES"){
		selector.style.left = no.clientWidth + "px";
		selector.style.width = yes.clientWidth + "px";
		selector.innerHTML = "YES";
		selector.style.backgroundColor = "#2daab8";
	}
}

function automationUpdateDisplayAutomatedButton(domain, value){
		// Handle new settings
		var no 			= document.getElementsByName(domain + "_automated_no")[0];
		var yes 		= document.getElementsByName(domain + "_automated_yes")[0];
		var selector 	= document.getElementsByName(domain + "_automated_selector")[0];
	
		if(value.toUpperCase() === "NO"){
			selector.style.left = 0;
			selector.style.width = no.clientWidth + "px";
			selector.style.backgroundColor = "#2daab8";
			selector.innerHTML = "NO";
		}else if(value.toUpperCase() === "YES"){
			selector.style.left = no.clientWidth + "px";
			selector.style.width = yes.clientWidth + "px";
			selector.innerHTML = "YES";
			selector.style.backgroundColor = "#2daab8";
		}
}

function automationSendSearchForm(){
	// Retrieve values from buttons
	param_search 		= document.getElementById('automation_search_button').value;
	param_legal 		= document.getElementById('automation_toggle_legal_selector').innerText;
	param_automated 	= document.getElementById('automation_toggle_automated_selector').innerText;
	// Update form
	document.getElementById('automation_form_search').value				= param_search;
	document.getElementById('automation_form_toggle_legal').value 		= param_legal;
	document.getElementById('automation_form_toggle_automated').value 	= param_automated;
	// Send form
	form = document.getElementById('automation_search_form');
	form.submit();
}

function automationUpdateSendForm(domain){
	// Retrieve is_interesting
	var is_legal 		= document.getElementsByName(domain + "_legal_selector")[0].innerHTML;
	var is_automated 	= document.getElementsByName(domain + "_automated_selector")[0].innerHTML;
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			displayNotification("Updated domain", domain)
		}
	};
	xhttp.open("POST", "/automation/target/update?domain=" + domain + "&is_legal=" + is_legal + "&is_automated=" + is_automated, true);
	xhttp.send();
}


/* ************************************ */
/*               SETTINGS               */
/* ************************************ */
function settingsSetMode(mode) {
	// Handle new settings
	var agressive	= document.getElementById("settings_toggle_mode_agressive");
	var passive		= document.getElementById("settings_toggle_mode_passive");
	var selector 	= document.getElementById("settings_toggle_mode_selector");

	if(mode.toUpperCase() === "AGRESSIVE"){
		selector.style.left = 0;
		selector.style.display = "block"
		selector.style.width = agressive.clientWidth + "px";
		selector.style.backgroundColor = "#2daab8";
		selector.innerHTML = "AGRESSIVE";
	}else if(mode.toUpperCase() === "PASSIVE"){
		selector.style.display = "block"
		selector.style.left = agressive.clientWidth + "px";
		selector.style.width = passive.clientWidth + "px";
		selector.innerHTML = "PASSIVE";
		selector.style.backgroundColor = "#2daab8";
	}
}

function settingsSendModeForm() {
	displayNotification("Switch mode", "Trying to change mode")
	mode = document.getElementById("settings_toggle_mode_selector").innerText;
	const req = new XMLHttpRequest();
	req.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			// Typical action to be performed when the document is ready:
			displayNotification("Switch mode", "Mode changed")
		}
	};
	req.open("POST", "/settings/update_mode?mode="+mode);
	req.send();
}

function settingsFileUploaded(){
	var name = document.getElementById('fileselector').files[0].name;
	document.getElementById('filename').innerText = name;
	document.getElementById('filename').hidden = false;
}

function settingsSendLock(){
	const req = new XMLHttpRequest();
	req.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			// Typical action to be performed when the document is ready:
			displayNotification("Lock", "Application locked")
		}
	};
	req.open("POST", "/settings/lock");
	req.send();
}


/* **************************************** */
/*               DATA DISPLAY               */
/* **************************************** */
function openModal(modal_id){
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
	url = "/data/get?id=" + id;

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
          openModal('data_viewer');
        }
      };

	// Send request
	update_form.send();
}


/* ***************************************** */
/*               NOTIFICATIONS               */
/* ***************************************** */
function displayNotification(title, description){
	setTimeout(function() {
		notification1 = document.getElementById("notification1");
		notification1_title = document.getElementById('notification1-title');
		notification1_description = document.getElementById('notification1-description');
		
		// if(notification1.classList.contains('notification-visible')){
		// 	notification1.classList.toggle('notification-visible');
		// }
		notification1.classList.toggle('notification-visible');
		notification1_title.innerHTML = '<strong>' + title + '</strong><br>'
		notification1_description.innerText = description
	}, 1000);
}